import os
import pathlib
import datetime

from django.test import TestCase, Client
from . import views
from .query_maker import QueryMaker
from .query_strategy import ExperimentQueryStrategy, DataSourceQueryStrategy
from .models import Experiment, DataSource

test_resources_path = '/test_resources/'


class ExperimentsearchTestCase(TestCase):

    def setUp(self):
        self.client = Client()
        resource_path = pathlib.Path(
            os.getcwd() + test_resources_path
        ).as_uri()
        views.data_source_url = resource_path + '/data_source/'
        views.experi_table_url = resource_path + '/experiment/'
        views.genotype_url = resource_path + '/genotype/'

    def test_url_build_1(self):
        url = 'www.foo.bar/?baz='
        search = "banana"
        expected = 'www.foo.bar/?baz=banana'
        actual = QueryMaker._make_query_url(url, search)
        self.assertEqual(expected, actual)

    def test_url_build_2(self):
        url = 'www.foo.bar/?baz='
        search = "banana cake"
        expected = 'www.foo.bar/?baz=banana+cake'
        actual = QueryMaker._make_query_url(url, search)
        self.assertEqual(expected, actual)

    def test_url_build_3(self):
        url = 'file://C:/foo bar/'
        search = "banana cake"
        expected = 'file://C:/foo bar/banana+cake'
        actual = QueryMaker._make_query_url(url, search)
        self.assertEqual(expected, actual)

    def test_experiment_query_1(self):
        expected_model = Experiment(
            name='What is up', primary_investigator='Badi James',
            data_source="data_source/?name=What+is+up",
            download_link='download/What+is+up/',
            date_created=datetime.datetime(
                2015, 11, 20, 11, 14, 40, 386012, datetime.timezone.utc
            )
        )
        expected_models = [expected_model]
        querier = QueryMaker(ExperimentQueryStrategy)
        actual_models = querier.make_query('bar.csv', views.experi_table_url)
        actual_model = actual_models[0]
        self.assertEqual(expected_model.data_source, actual_model.data_source)
        self.assertEqual(expected_model.download_link, actual_model.download_link)
        self.assertEqual(expected_model.name, actual_model.name)
        self.assertEqual(
            expected_model.primary_investigator, actual_model.primary_investigator
        )
        self.assertEqual(expected_model.date_created, actual_model.date_created)

    def test_data_source_query_1(self):
        expected_model = DataSource(
            name= 'What is up', supplier='Badi James', is_active='False',
            source='testgzpleaseignore.gz',
            supply_date=datetime.date(2015, 11, 18),
        )
        querier = QueryMaker(DataSourceQueryStrategy)
        actual_models = querier.make_query('foo.csv', views.data_source_url)
        actual_model = actual_models[0]
        self.assertEqual(expected_model.name, actual_model.name)
        self.assertEqual(expected_model.source, actual_model.source)
        self.assertEqual(expected_model.supplier, actual_model.supplier)
        self.assertEqual(expected_model.supply_date, actual_model.supply_date)
        self.assertEqual(expected_model.is_active, actual_model.is_active)


