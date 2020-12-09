from decimal import *

from .repository import PayrollRepository


class PayrollService:
    MONTH_HOURS = 168
    EXTRA_HOUR_PERCENTAGE = 50

    def __init__(self, repository: PayrollRepository):
        self.repository = repository

    @staticmethod
    def get_instance(repository: PayrollRepository):
        return PayrollService(repository)

    def make_payment(self, log_work):
        hours = log_work['hours']
        rate = log_work['rate']
        worked_hours = self.__calculate_extra_hours(hours)
        payment = self.__calculate_payment(worked_hours, rate)
        payment = {
            'month': log_work['month'],
            'employee_id': log_work['employee_id'],
            'rate': rate,
            'worked_hours': worked_hours,
            'payment': payment
        }
        self.repository.save(payment)
        return payment

    def __calculate_extra_hours(self, total):
        normal = total
        extra = 0
        if total > self.MONTH_HOURS:
            normal = self.MONTH_HOURS
            extra = total - self.MONTH_HOURS
        return {
            'total': total,
            'normal': normal,
            'extra': extra
        }

    def __calculate_payment(self, worked_hours, rate):
        decimal_rate = Decimal(str(rate))
        decimal_extra_hours = Decimal(str(worked_hours['extra']))

        normal_payment = Decimal(str(worked_hours['normal'])) * decimal_rate

        extra_payment = decimal_extra_hours * decimal_rate + \
                        ((decimal_extra_hours * self.EXTRA_HOUR_PERCENTAGE / 100) * decimal_rate)

        total_payment = normal_payment + extra_payment

        return {
            'total': float(total_payment),
            'normal': float(normal_payment),
            'extra': float(extra_payment)
        }
