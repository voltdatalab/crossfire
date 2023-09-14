from datetime import datetime, timedelta

from decouple import UndefinedValueError, config
from pandas import DataFrame
from requests import get, post

from crossfire.errors import CrossfireError


class CredentialsNotFoundError(CrossfireError):
    def __init__(self, key):
        message = f"There's no enviornment variable `{key}` condigured."
        super().__init__(message)


class IncorrectCrdentialsError(CrossfireError):
    pass


def to_dataframe(resp):
    resp.encoding = "utf8"
    contents = resp.json()
    return DataFrame(contents.get("data", []))


class Token:
    def __init__(self, value, expires_in):
        self.value = value
        self.valid_until = datetime.now() + timedelta(seconds=expires_in)

    def is_valid(self):
        return datetime.now() < self.valid_until


class Client:
    URL = "https://api-service.fogocruzado.org.br/api/v2/"

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

        url = f"{self.URL}auth/login"
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

    def get(self, *args, **kwargs):
        """Wraps requests.get to inject the authorization header."""
        auth = {"Authorization": f"Bearer {self.token}"}

        if "headers" not in kwargs:
            kwargs["headers"] = auth
        else:
            kwargs["headers"].update(auth)

        return get(*args, **kwargs)

    def states(self, as_dataframe=True):
        resp = self.get(f"{self.URL}states")
        if as_dataframe:
            return to_dataframe(resp)

        return resp.json().get("data", [])
