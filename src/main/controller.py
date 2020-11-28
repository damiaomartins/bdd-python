from flask import Flask
from flask.views import MethodView

from .service import EmployeeService


class EmployeeController:
    def __init__(self, app: Flask, service: EmployeeService):
        app.add_url_rule('/employee/', view_func=AddEmployeeView.as_view('AddEmployeeView', service))
        app.add_url_rule('/employee/<id>', view_func=AddEmployeeView.as_view('UpdateEmployeeView', service))


class AddEmployeeView(MethodView):
    def __init__(self, service: EmployeeService):
        self.service = service

    def get(self, id=None):
        self.service.add({'id': id})
        return 'ok'
