from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse

def home_view(request):
    return HttpResponseRedirect(reverse('polls:question-detail', args=(3,)))