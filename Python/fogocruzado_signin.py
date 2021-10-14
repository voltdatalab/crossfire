import os

from Python.fogocruzado_utils import get_token_fogocruzado


def fogocruzado_signin(email, password):
    """
    Function to  login to fogocruzado API
    :param email: string
        User e-mail registered in the fogocruzado API
    :param password: string
        User password registered in the fogocruzado API
    :return:
        None
    Example
    -------
    >>> from crossfire import fogocruzado_signin
    >>> fogocruzado_signin(email='user@host.com', password='password')
    """

    os.environ['FOGO_CRUZADO_EMAIL'] = email
    os.environ['FOGO_CRUZADO_PASSWORD'] = password

    get_token_fogocruzado()
