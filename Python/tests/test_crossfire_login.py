from unittest import TestCase
import os
from fogocruzado_signin import fogocruzado_signin
from decouple import config


class TestBadLogin(TestCase):
    def setUp(self):
        self.bad_signin = fogocruzado_signin('email@host.com', 'password')

    def test_fogocruzado_login_environment_variable(self):
        """assert the parameters passed to fogocruzado_signin are correctly accessed in the environment"""
        self.assertEqual(os.getenv("FOGO_CRUZADO_EMAIL"), 'email@host.com')
        self.assertEqual(os.getenv("FOGO_CRUZADO_PASSWORD"), 'password')


class TestSuccessLogin(TestCase):
    def setUp(self):
        self.right_signin = fogocruzado_signin(config('FOGO_CRUZADO_EMAIL'), config('FOGO_CRUZADO_PASSWORD'))

    def test_get_token_status_code(self):
        """asset message != Unauthorized"""
        self.assertTrue(os.environ["FOGO_CRUZADO_API_TOKEN"])
