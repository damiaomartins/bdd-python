from .repository import EmployeeRepository


class EmployeeService:
    def __init__(self, repository: EmployeeRepository):
        self.repository = repository

    def add(self, employee):
        self.repository.save(employee)
