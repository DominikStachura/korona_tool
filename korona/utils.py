import random
import string
import os

from django.contrib.auth.models import User
from django.http import HttpResponse



def random_string_generator(size=5, chars=string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def unique_code_generator():
    new_code = random_string_generator()
    while User.objects.all().filter(password=new_code).first() is not None:
        new_code = random_string_generator()

    return new_code


