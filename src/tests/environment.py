from unittest import mock

from behave import fixture, use_fixture

from src.main import app


@fixture
def setup_environment(context, *args, **kwargs):
    with mock.patch('src.main.repository.EmployeeRepository') as repository:
        repository_mock = mock.Mock()
        repository.get_instance.return_value = repository_mock
        flask_app = app.create_app()
        flask_app.testing = True
        context.client = flask_app.test_client()
        context.repository = repository_mock
    yield context.client


def before_feature(context, feature):
    # recreate the app for every feature
    use_fixture(setup_environment, context)
