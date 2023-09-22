from datetime import datetime, timedelta
from urllib.parse import urlencode

from decouple import UndefinedValueError, config
from requests import get, post

from crossfire.errors import CrossfireError
from crossfire.parser import parse_response


class CredentialsNotFoundError(CrossfireError):
    def __init__(self, key):
        message = f"There's no enviornment variable `{key}` condigured."
        super().__init__(message)


class IncorrectCrdentialsError(CrossfireError):
    pass


class Token:
    def __init__(self, value, expires_in):
        self.value = value
        self.valid_until = datetime.now() + timedelta(seconds=expires_in)

    def is_valid(self):
        return datetime.now() < self.valid_until


class Client:
    URL = "https://api-service.fogocruzado.org.br/api/v2"

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

        url = f"{self.URL}/auth/login"
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
        return self.get(f"{self.URL}/states", format=format)

    def cities(self, city_id=None, city_name=None, state_id=None, format=None):
        params = {"cityId": city_id, "cityName": city_name, "stateId": state_id}
        cleaned = urlencode({key: value for key, value in params.items() if value})
        return self.get(f"{self.URL}/cities?{cleaned}", format=format)

    def occurrences(
        self,
        city_id=None,
        state_id=None,
        initial_date=None,
        final_date=None,
        format=None,
    ):
        params = {
            "idCities": city_id,
            "idState": state_id,
            "initialdate": initial_date,
            "finaldate": final_date,
        }
        cleaned = urlencode({key: value for key, value in params.items() if value})
        return self.get(f"{self.URL}/occurrences?{cleaned}", format=format)
