import sys
from math import factorial

from celery import shared_task
sys.set_int_max_str_digits(10000000)


@shared_task
def add(x):
    result = factorial(x)
    print(result)
    return result
