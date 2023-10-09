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
    MAX_PARALLEL_REQUESTS = 32

    def __init__(self, email=None, password=None, max_parallel_requests=None):
        try:
            self.email = email or config("FOGOCRUZADO_EMAIL")
        except UndefinedValueError:
            raise CredentialsNotFoundError("FOGOCRUZADO_EMAIL")

        try:
            self.password = password or config("FOGOCRUZADO_PASSWORD")
        except UndefinedValueError:
            raise CredentialsNotFoundError("FOGOCRUZADO_PASSWORD")

        self.max_parallel_requests = max_parallel_requests or self.MAX_PARALLEL_REQUESTS
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

    def _states(self, format=None):
        return self.get(f"{self.URL}/states", format=format)

    def states(self, *args, **kwargs):
        states, _ = self._states(*args, **kwargs)
        return states

    def _cities(self, city_id=None, city_name=None, state_id=None, format=None):
        params = {"cityId": city_id, "cityName": city_name, "stateId": state_id}
        cleaned = urlencode({key: value for key, value in params.items() if value})
        return self.get(f"{self.URL}/cities?{cleaned}", format=format)

    def cities(self, *args, **kwargs):
        cities, _ = self._cities(*args, **kwargs)
        return cities
