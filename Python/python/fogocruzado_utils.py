import json
import os
import sys

import requests


def get_token_fogocruzado():
    """Get token from Fogo Cruzado's API"""
    post_fogocruzado = requests.post(
        "https://api.fogocruzado.org.br/api/v1/auth/login",
        data={'email': os.getenv("FOGO_CRUZADO_EMAIL"),
              'password': os.getenv("FOGO_CRUZADO_PASSWORD")}
    )
    access_fogocruzado = json.loads(post_fogocruzado.content).get('access_token')
    accesstoken_fogocruzado = f"Bearer {access_fogocruzado}"

    if access_fogocruzado != "Unauthorized":
        os.environ["FOGO_CRUZADO_API_TOKEN"] = accesstoken_fogocruzado
    else:
        sys.exit(
            "These credentials do not correspond to Fogo Cruzado's records. \nPlease check your e-mail and password or access https://api.fogocruzado.org.br/register to register.")
