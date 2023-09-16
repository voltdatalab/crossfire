from datetime import datetime, timedelta

from decouple import UndefinedValueError, config
from requests import get, post
from urllib.parse import urlencode
from crossfire.errors import CrossfireError

try:
    from pandas import DataFrame

    HAS_PANDAS = True
except ModuleNotFoundError:
    HAS_PANDAS = False


URL = "https://api-service.fogocruzado.org.br/api/v2"
FORMATS = {"df", "dict"}


class CredentialsNotFoundError(CrossfireError):
    def __init__(self, key):
        message = f"There's no enviornment variable `{key}` condigured."
        super().__init__(message)


class IncorrectCrdentialsError(CrossfireError):
    pass


class UnknownFormatError(CrossfireError):
    def __init__(self, format):
        message = f"Unknown format `{format}`. Valid formats are: {', '.join(FORMATS)}"
        super().__init__(message)


class Token:
    def __init__(self, value, expires_in):
        self.value = value
        self.valid_until = datetime.now() + timedelta(seconds=expires_in)

    def is_valid(self):
        return datetime.now() < self.valid_until


def parse_response(method):
    def wrapper(self, *args, **kwargs):
        """Converts API response to a dicitonary, Pandas DataFrame or GeoDataFrame."""
        format = kwargs.pop("format", None)
        if format and format not in FORMATS:
            raise UnknownFormatError(format)

        response = method(self, *args, **kwargs)
        response.encoding = "utf8"
        contents = response.json()
        data = contents.get("data", [])

        if HAS_PANDAS and format in ("df", None):
            return DataFrame(data)

        return data

    return wrapper


class Client:
    def __init__(self, **kwargs):
        self.email = kwargs.get("email")
        self.password = kwargs.get("password")
        if self.email is None:
            try:
                self.email = config("FOGOCRUZADO_EMAIL")
            except UndefinedValueError:
                raise CredentialsNotFoundError("FOGOCRUZADO_EMAIL")
        if self.password is None:
            try:
                self.password = kwargs.get("password", config("FOGOCRUZADO_PASSWORD"))
            except UndefinedValueError:
                raise CredentialsNotFoundError("FOGOCRUZADO_PASSWORD")

        self.cached_token = None

    @property
    def token(self):
        if self.cached_token and self.cached_token.is_valid():
            return self.cached_token.value

        url = f"{URL}/auth/login"
        resp = post(url, json={"email": self.email, "password": self.password})
        if resp.status_code == 401:
            data = resp.json()
            raise IncorrectCrdentialsError(data["msg"])

        if resp.status_code != 201:
            resp.raise_for_status()

        data = resp.json()
        self.cached_token = Token(
            data["data"]["accessToken"], data["data"]["expiresIn"]
        )
        return self.cached_token.value

    @parse_response
    def get(self, *args, **kwargs):
        """Wraps `requests.get` to inject the authorization header. Also, accepts the
        `format` argument consumed by the `parse_response` decorator, which removes it
        before passing the arguments to `requests.get`."""
        auth = {"Authorization": f"Bearer {self.token}"}

        if "headers" not in kwargs:
            kwargs["headers"] = auth
        else:
            kwargs["headers"].update(auth)

        return get(*args, **kwargs)

    def states(self, format=None):
        return self.get(f"{URL}/states", format=format)

    def cities(self, uuid=None, name=None, state_uuid=None, format=None):
        city_url = f"{URL}/cities"
        filters = {}
        if uuid:
            filters.update({"cityId": uuid})
        if name:
            filters.update({"cityName": name})
        if state_uuid:
            filters.update({"stateId": state_uuid})
        return self.get(city_url, urlencode(filters), format=format)
