import logging

from behave import given, when, then

from src.main import main

logging.basicConfig(
    format='[%(levelname)s] %(message)s',
    level=logging.DEBUG
)


@given('o ambiente de testes esteja configurado')
def step_impl(context):
    print('setup')


@given('given')
def step_impl(context):
    logging.info(f'given: {main.teste}')


@when('when')
def step_impl(context):
    print('when')


@then('then')
def step_impl(context):
    print('then')
