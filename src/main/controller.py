import json
import logging

from flask import Flask, request, make_response
from flask.views import MethodView

from .service import PayrollService


class PayrollController:
    def __init__(self, app: Flask, service: PayrollService):
        app.add_url_rule('/payroll', view_func=PayrollView.as_view('PayrollView', service))


class PayrollView(MethodView):
    def __init__(self, service: PayrollService):
        self.service = service

    def post(self):
        response = {}
        try:
            log_work = self.__parse_log_work(request.data)
            response['data'] = self.service.make_payment(log_work)
        except AttributeError as e:
            logging.error(e)
            response['error'] = e.args[0]
            return make_response(response, 400)
        except Exception as e:
            logging.error(e)
            response['error'] = 'Internal error'
            return make_response(response, 500)
        return make_response(response)

    def __parse_log_work(self, data):
        log_work = json.loads(data)
        self.__validate(log_work)
        return log_work

    def __validate(self, log_work):
        self.__validate_attribute(log_work, 'employee_id')
        self.__validate_attribute(log_work, 'month')
        self.__validate_attribute(log_work, 'hours', custom_validator=lambda x: x > 0)
        self.__validate_attribute(log_work, 'rate', custom_validator=lambda x: x > 0)

    def __validate_attribute(self, log_work, name, custom_validator=lambda x: True):
        actual_value = log_work.get(name)
        if not actual_value or not custom_validator(actual_value):
            raise AttributeError(f'Invalid attribute: {name}')
