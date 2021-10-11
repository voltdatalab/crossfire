import os
from unittest import TestCase

from decouple import config

from fogocruzado_signin import fogocruzado_signin


class TestSuccessLogin(TestCase):
    def setUp(self):
        self.right_signin = fogocruzado_signin(config('FOGO_CRUZADO_EMAIL'), config('FOGO_CRUZADO_PASSWORD'))

    def test_fogocruzado_login_environment_variable(self):
        """assert the parameters passed to fogocruzado_signin enables FOGO_CRUZADO varibale in the environment"""
        self.assertTrue(os.environ["FOGO_CRUZADO_API_TOKEN"])
