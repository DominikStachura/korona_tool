import random
import string
from winreg import *
from django.contrib.auth.models import User


def random_string_generator(size=5, chars=string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def unique_code_generator():
    new_code = random_string_generator()
    while User.objects.all().filter(password=new_code).first() is not None:
        new_code = random_string_generator()

    return new_code


def get_download_path():
    with OpenKey(HKEY_CURRENT_USER, 'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders') as key:
        Downloads = QueryValueEx(key, '{374DE290-123F-4565-9164-39C4925E467B}')[0]
    return Downloads
