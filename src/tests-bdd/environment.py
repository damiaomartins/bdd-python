from unittest import mock

from behave import fixture, use_fixture

from src.main import app


@fixture
def setup_environment(context, *args, **kwargs):
    with mock.patch('src.main.repository.PayrollRepository') as repository:
        repository.return_value = repository
        flask_app = app.create_app()
        flask_app.testing = True
        context.client = flask_app.test_client()
        context.mock_repository = repository
    yield context.client


def before_feature(context, feature):
    use_fixture(setup_environment, context)
