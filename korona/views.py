from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .utils import unique_code_generator
from polls.models import History


def home_view(request):
    logout(request)
    context = {}
    if request.method == 'POST':
        # if 'password' in request.POST:
        #     password = request.POST.get('password')
        #     user = User.objects.all().filter(username=request.POST.get('password'))
        #     if user.exists():
        #         user = user.first()
        #         login(request, user)
        #         history = History(code=password)
        #         history.assigned_user = user
        #         history.save()
        #         return HttpResponseRedirect(reverse('polls:question-detail', args=(3,)))
        #     else:
        #         context['message'] = 'Brak danych przypisanych do kodu'
        # else:
            code = unique_code_generator()
            user = User(username=code, password=code)
            user.save()
            history = History(code=code)
            history.assigned_user = user
            history.save()
            login(request, user)
            return HttpResponseRedirect(reverse('polls:intro'))
    return render(request, 'home.html', context=context)


def intro_login_view(request):
    logout(request)
    context = {}
    if request.method == 'POST':
        if 'password' in request.POST:
            password = request.POST.get('password')
            user = User.objects.all().filter(username=request.POST.get('password'))
            if user.exists():
                user = user.first()
                login(request, user)
                history = History(code=password)
                history.assigned_user = user
                history.save()
                return HttpResponseRedirect(reverse('polls:question-detail', args=(3,)))
            else:
                context['message'] = 'Brak danych przypisanych do kodu'
    return render(request, 'intro_login.html', context=context)

