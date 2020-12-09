import json
import logging
from datetime import datetime, timedelta

from behave import given, when, then
from hamcrest import *

logging.basicConfig(
    format='[%(levelname)s] %(message)s',
    level=logging.DEBUG
)


@given('o ambiente de testes esteja configurado')
def step_impl(context):
    context.mock_repository.reset_mock()


@given('O funcionário {employee_id} que recebe {rate} reais por hora, submeteu um total de {hours} horas no último mes')
def step_impl(context, employee_id, rate, hours):
    last_month = datetime.now().replace(day=1) - timedelta(days=1)
    context.request = {
        "month": last_month.strftime("%Y%m"),
    }
    __add_atribute_to_request(context.request, 'employee_id', employee_id, str)
    __add_atribute_to_request(context.request, 'hours', hours, float)
    __add_atribute_to_request(context.request, 'rate', rate, float)


def __add_atribute_to_request(request, name, value_str, type):
    if value_str == "{vazio}":
        request[name] = ''
    elif value_str != "{not_set}":
        request[name] = type(value_str)


@when('For executada o sistema de pagamento')
def step_impl(context):
    context.response = context.client.post('/payroll', data=json.dumps(context.request))


@then(
    'O pagamento do funcionário dará um total de {total} reais, sendo {normal} de horas normais e {extra} de horas extras')
def step_impl(context, total, normal, extra):
    assert_that(context.response.status_code, equal_to(200))

    response_data = json.loads(context.response.data)
    assert_that(response_data.get('error'), none())
    assert_that(response_data.get('data'), not_none())

    payment_details = response_data['data']
    assert_that(payment_details['payment']['normal'], equal_to(float(normal)), "Horas normais")
    assert_that(payment_details['payment']['extra'], equal_to(float(extra)), "Horas extras")
    assert_that(payment_details['payment']['total'], equal_to(float(total)), "Valor total")

    assert_that(payment_details['month'], equal_to(context.request['month']), "Mês")
    assert_that(payment_details['employee_id'], equal_to(context.request['employee_id']), "Id funcionário")
    assert_that(payment_details['rate'], equal_to(context.request['rate']), "Valor/hora")

    assert_that(context.mock_repository.save.call_count, equal_to(1))


@then('A solicitação falhará com uma mensagem de erro')
def step_impl(context):
    assert_that(context.response.status_code, is_not(equal_to(200)))

    response_data = json.loads(context.response.data)
    assert_that(response_data.get('data'), none())
    assert_that(response_data.get('error'), not_none())
    assert_that(response_data.get('error'), is_not(empty()))

    assert_that(context.mock_repository.save.call_count, equal_to(0))
