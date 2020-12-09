import logging


class PayrollRepository:
    def __init__(self):
        pass

    @staticmethod
    def get_instance():
        return PayrollRepository()

    def save(self, payment):
        logging.error(f'Saving payment={payment}')
