from django.db import models

# Create your models here.

import datetime

from django.db import models
from django.utils import timezone


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    numerical_value = models.FloatField(null=True, blank=True)
    next_question = models.ForeignKey("self", on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    final = models.BooleanField(default=False)

    def __str__(self):
        return self.choice_text


class ChoiceOrder(models.Model):
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    # zrobic string pytan i string odpowiedzi i na koniec je rozdzielac do tablicy i do csv