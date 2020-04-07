import random
import string
from django.contrib.auth.models import User
from polls.models import History
from io import BytesIO
import xlsxwriter


def random_string_generator(size=5, chars=string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def unique_code_generator():
    new_code = random_string_generator()
    while User.objects.all().filter(password=new_code).first() is not None:
        new_code = random_string_generator()

    return new_code


def create_spreadsheet_data(code):
    history = History.objects.all().filter(code=code)
    if history.exists():
        output = BytesIO()
        workbook = xlsxwriter.Workbook(output)
        for index, history_instance in enumerate(history):
            if history_instance.answers_all is not None:
                row = 0
                col = 0
                worksheet = workbook.add_worksheet(f'{history_instance.pub_date.strftime("%Y%m%d-%H%M%S")}')
                for q, a in zip(history_instance.questions_all.split('||')[1:], history_instance.answers_all.split('||')[1:]):
                    worksheet.write(row, col, q)
                    worksheet.write(row, col + 1, a)
                    row += 1
        workbook.close()
        return output.getvalue()
    return None
