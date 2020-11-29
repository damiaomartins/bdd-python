import logging


class EmployeeRepository:
    def __init__(self):
        pass

    def save(self, employee):
        logging.info(employee)

    @staticmethod
    def get_instance():
        return EmployeeRepository()
