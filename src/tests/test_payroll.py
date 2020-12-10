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

    assert_that(response_data.get('error'), none())
    assert_that(response_data.get('data'), not_none())

    payment_details = response_data['data']
    assert_that(payment_details['month'], equal_to(expected_response['month']))
    assert_that(payment_details['employee_id'], equal_to(expected_response['employee_id']))
    assert_that(payment_details['rate'], equal_to(expected_response['rate']))

    assert_that(payment_details['payment']['normal'], equal_to(expected_response['payment']['normal']))
    assert_that(payment_details['payment']['extra'], equal_to(expected_response['payment']['extra']))
    assert_that(payment_details['payment']['total'], equal_to(expected_response['payment']['total']))


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

