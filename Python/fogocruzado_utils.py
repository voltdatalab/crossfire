import json
import os

import requests


def get_token_fogocruzado():
    """Get token from Fogo Cruzado's API"""
    try:
        post_fogocruzado = requests.post(
            "https://api.fogocruzado.org.br/api/v1/auth/login",
            data={'email': os.getenv("FOGO_CRUZADO_EMAIL"),
                  'password': os.getenv("FOGO_CRUZADO_PASSWORD")}
        )
        access_fogocruzado = json.loads(post_fogocruzado.content).get('access_token')
        accesstoken_fogocruzado = f"Bearer {access_fogocruzado}"
        os.environ["FOGO_CRUZADO_API_TOKEN"] = accesstoken_fogocruzado
        post_fogocruzado.raise_for_status()

    except requests.exceptions.HTTPError:
        raise SystemExit(
            "These credentials do not correspond to Fogo Cruzado's records. \nPlease check your e-mail and password or access https://api.fogocruzado.org.br/register to register.")
