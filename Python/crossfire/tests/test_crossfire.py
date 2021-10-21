import os
from datetime import date
from unittest import TestCase

import numpy
from crossfire.fogocruzado_signin import fogocruzado_signin
from crossfire.fogocruzado_utils import fogocruzado_key, extract_data_api, extract_cities_api
from crossfire.get_cities import get_cities
from crossfire.get_fogocruzado import get_fogocruzado
from decouple import config
from geopandas import GeoDataFrame
from pandas import DataFrame


class TestSuccessSignin(TestCase):
    def setUp(self):
        fogocruzado_signin(config('FOGO_CRUZADO_EMAIL'), config('FOGO_CRUZADO_PASSWORD'))

    def test_fogocruzado_signin_environment_variable(self):
        """
        assert the parameters passed to fogocruzado_signin enables FOGO_CRUZADO varibale
        in the environment
        """
        self.assertTrue(os.environ["FOGO_CRUZADO_EMAIL"])
        self.assertTrue(os.environ["FOGO_CRUZADO_PASSWORD"])
        self.assertTrue(os.environ["FOGO_CRUZADO_API_TOKEN"])


class TestFogoCruzadoKey(TestCase):
    """
    Asserts that with right environmental variables a key is returned from API
    """

    def setUp(self):
        fogocruzado_signin(config('FOGO_CRUZADO_EMAIL'), config('FOGO_CRUZADO_PASSWORD'))
        self.key = fogocruzado_key()

    def test_environmental_variable_is_not_none(self):
        self.assertIsNotNone(self.key)


class TestExtractDataAPI(TestCase):
    def setUp(self):
        fogocruzado_signin(config('FOGO_CRUZADO_EMAIL'), config('FOGO_CRUZADO_PASSWORD'))

    def test_extract_data_api(self):
        self.data = extract_data_api(
            link='https://api.fogocruzado.org.br/api/v1/occurrences?data_ocorrencia[gt]=2020-01-01&data_ocorrencia[lt]=2020-02-01'
        )
        self.assertIsInstance(self.data, DataFrame)
        self.assertTrue(self.data is not None)


class TestExtractCitiesAPI(TestCase):
    def setUp(self):
        fogocruzado_signin(config('FOGO_CRUZADO_EMAIL'), config('FOGO_CRUZADO_PASSWORD'))

    def test_extract_cities_api(self):
        self.data = extract_cities_api()
        self.assertIsInstance(self.data, DataFrame)
        self.assertTrue(self.data is not None)


class TestGetCitiesAPI(TestCase):
    def setUp(self):
        fogocruzado_signin(config('FOGO_CRUZADO_EMAIL'), config('FOGO_CRUZADO_PASSWORD'))
        self.cities = get_cities()

    def test_extract_cities_api(self):
        self.assertIsInstance(self.cities, DataFrame)
        self.assertTrue(self.cities is not None)
        self.assertIsInstance(type(self.cities.DensidadeDemografica[0]), type(numpy.float64))


class TestGetFogoCruzado(TestCase):
    def setUp(self):
        fogocruzado_signin(config('FOGO_CRUZADO_EMAIL'), config('FOGO_CRUZADO_PASSWORD'))

    def test_sucessful_get_fogocruzado(self):
        self.sucessful_get_fogocruzado = get_fogocruzado()
        self.assertIsInstance(self.sucessful_get_fogocruzado, GeoDataFrame)

    def test_unsucessful_get_fogocruzado(self):
        self.sucessful_get_fogocruzado = get_fogocruzado(initial_date=date(2020, 1, 1), final_date=date(2021, 10, 1))
        self.assertFalse(self.sucessful_get_fogocruzado)


class TestFilterCityFogoCruzado(TestCase):
    def setUp(self):
        fogocruzado_signin(config('FOGO_CRUZADO_EMAIL'), config('FOGO_CRUZADO_PASSWORD'))

    def test_sucessful_filter_city_from_string(self):
        self.sucessful_get_fogocruzado = get_fogocruzado(city="Rio de Janeiro")
        self.assertTrue(
            self.sucessful_get_fogocruzado.nome_cidade.unique()[0] == 'Rio de Janeiro'
        )

    def test_sucessful_filter_city_from_list(self):
        self.sucessful_get_fogocruzado = get_fogocruzado(city=['Rio de Janeiro', 'Belford Roxo'])
        self.assertTrue(
            list(self.sucessful_get_fogocruzado.nome_cidade.unique()) == ['Rio de Janeiro', 'Belford Roxo']
        )

    def test_sucessful_filter_state_from_string(self):
        self.sucessful_get_fogocruzado = get_fogocruzado(state="RJ")
        self.assertTrue(
            self.sucessful_get_fogocruzado.uf_estado.unique()[0] == 'RJ'
        )

    def test_sucessful_filter_state_from_list(self):
        self.sucessful_get_fogocruzado = get_fogocruzado(state=['RJ', 'PE'])
        self.assertTrue(
            list(self.sucessful_get_fogocruzado.uf_estado.unique()) == ['RJ', 'PE']
        )

    def test_sucessful_filter_security_agent_from_string(self):
        self.sucessful_get_fogocruzado = get_fogocruzado(security_agent=1)
        self.assertTrue(
            self.sucessful_get_fogocruzado.presen_agen_segur_ocorrencia.unique()[0] == 1
        )

    def test_sucessful_filter_security_agent_from_list(self):
        self.sucessful_get_fogocruzado = get_fogocruzado(security_agent=[0, 1])
        self.assertTrue(
            list(self.sucessful_get_fogocruzado.presen_agen_segur_ocorrencia.unique()) == [0, 1]
        )