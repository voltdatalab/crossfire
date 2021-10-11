import os

from fogocruzado_utils import get_token_fogocruzado


def fogocruzado_signin(email, password):
    """
    Function to  login to fogocruzado API
    :param email: User e-mail registered in the fogocruzado API
    :param password: User password registered in the fogocruzado API
    :return:
    """
    os.environ['FOGO_CRUZADO_EMAIL'] = email
    os.environ['FOGO_CRUZADO_PASSWORD'] = password

    get_token_fogocruzado()
