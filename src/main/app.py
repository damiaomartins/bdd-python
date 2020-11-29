import logging

from flask import Flask

from .controller import EmployeeController
from .repository import EmployeeRepository
from .service import EmployeeService

teste = 'abc'


def create_app() -> Flask:
    logging.basicConfig(
        format='[%(asctime)s][%(levelname)s] %(message)s',
        level=logging.INFO
    )
    app = Flask(__name__)
    repository = EmployeeRepository.get_instance()
    service = EmployeeService.get_instance(repository)
    EmployeeController(app, service)
    return app


print('main loaded')
