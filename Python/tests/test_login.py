import os
from unittest import TestCase

from decouple import config

from fogocruzado_signin import fogocruzado_signin
from fogocruzado_utils import fogocruzado_key

class TestSuccessLogin(TestCase):
    def setUp(self):
        self.right_signin = fogocruzado_signin(config('FOGO_CRUZADO_EMAIL'), config('FOGO_CRUZADO_PASSWORD'))

    def test_fogocruzado_login_environment_variable(self):
        """assert the parameters passed to fogocruzado_signin enables FOGO_CRUZADO varibale in the environment"""
        self.assertTrue(os.environ["FOGO_CRUZADO_API_TOKEN"])

class TestFogoCruzaadoKey(TestCase):
    def setUp(self):
        fogocruzado_signin(config('FOGO_CRUZADO_EMAIL'), config('FOGO_CRUZADO_PASSWORD'))
        self.fogocruzado_key = fogocruzado_key()

    def test_environmental_variable_is_not_none(self):
        self.assertIsNotNone(self.fogocruzado_key)
