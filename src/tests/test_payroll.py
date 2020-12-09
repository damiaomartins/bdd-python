import json
from unittest import mock

import pytest
from hamcrest import *

from src.main import app


@pytest.fixture
def client():
    with mock.patch('src.main.repository.PayrollRepository') as repository:
        repository.return_value = repository
        flask_app = app.create_app()
        flask_app.testing = True
        client = flask_app.test_client()
    yield client


def test_successful_payment(client):
    request = {
        "employee_id": "123",
        "month": "202011",
        "hours": 200,
        "rate": 30
    }

    response = client.post('/payroll', data=json.dumps(request))
    response_data = json.loads(response.data)

    expected_response = {
        "employee_id": request['employee_id'],
        "month": request['month'],
        "rate": request['rate'],
        "payment": {
            "extra": 1440,
            "normal": 5040,
            "total": 6480
        }
    }
    assert_that(response.status_code, equal_to(200))
    __assert_payment_response(response_data, expected_response)


def test_invalid_rate(client):
    request = {
        "employee_id": "123",
        "month": "202011",
        "hours": 200
    }

    response = client.post('/payroll', data=json.dumps(request))
    response_data = json.loads(response.data)

    assert_that(response.status_code, equal_to(400))
    __assert_error_response(response_data)


def test_invalid_hours(client):
    request = {
        "employee_id": "123",
        "month": "202011",
        "hours": -200,
        "rate": 30
    }

    response = client.post('/payroll', data=json.dumps(request))
    response_data = json.loads(response.data)

    assert_that(response.status_code, equal_to(400))
    __assert_error_response(response_data)


def __assert_error_response(response_data):
    assert_that(response_data.get('error'), is_not(None))
    assert_that(response_data.get('data'), is_(None))


def __assert_payment_response(actual, expected):
    assert_that(actual.get('error'), is_(None))
    assert_that(actual.get('data'), is_not(None))

    payment_details = actual['data']
    assert_that(payment_details['month'], expected['month'])
    assert_that(payment_details['employee_id'], expected['employee_id'])
    assert_that(payment_details['rate'], expected['rate'])

    assert_that(payment_details['payment']['normal'], expected['payment']['normal'])
    assert_that(payment_details['payment']['extra'], expected['payment']['extra'])
    assert_that(payment_details['payment']['total'], expected['payment']['total'])
