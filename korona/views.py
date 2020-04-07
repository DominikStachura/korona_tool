from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from .utils import unique_code_generator
from polls.models import History


def home_view(request):
    # user = User(username='user', password='1234')
    # user.save()
    # print(User.objects.all().filter(password='1234').exists())

    # print(request.user.is_authenticated)
    logout(request)
    # code = unique_code_generator()
    # context = {'code': code}
    # history = History(code=code)
    # history.save()
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
        else:
            code = unique_code_generator()
            user = User(username=code, password=code)
            user.save()
            history = History(code=code)
            history.assigned_user = user
            history.save()
            login(request, user)
            return HttpResponseRedirect(reverse('polls:intro'))
    return render(request, 'home.html', context=context)


def login_view(request):
    # form = LoginForm(request.POST or None)
    # context = {"form": form}
    # print(request.user.is_authenticated)
    if request.method == 'POST':
        # print(User.objects.all().filter(username='user').exists())
        # print(request.POST.get('password'))
        # user = authenticate(request, username='user',
        #                     password=request.POST.get('password'))
        user = User.objects.all().filter(password=request.POST.get('password')).first()
        if user is not None:
            print("Logged in")
            login(request, user)
            # context["form"] = LoginForm()  # zeby wyczyscilo dane
            redirect("/")
            # return HttpResponseRedirect(reverse('polls:question-detail', args=(3,)))
        else:
            print("error")

    return render(request, "login.html")
