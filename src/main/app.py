import logging

from flask import Flask

from .controller import PayrollController
from .repository import PayrollRepository
from .service import PayrollService


def create_app() -> Flask:
    logging.basicConfig(
        format='[%(asctime)s][%(levelname)s] %(message)s',
        level=logging.INFO
    )
    app = Flask(__name__)
    repository = PayrollRepository.get_instance()
    service = PayrollService.get_instance(repository)
    PayrollController(app, service)
    return app


print('main loaded')
