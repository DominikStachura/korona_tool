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
    code = unique_code_generator()
    context = {'code': code}
    history = History(code=code)
    history.save()

    if request.method == 'POST':
        password = request.POST.get('password')
        history = History.objects.all().filter(code=password)
        if history.exists():
            user = User(username=password, password=password)
            user.save()
            login(request, user)
            instance = history.first()
            instance.assigned_user = user
            instance.save()
            return HttpResponseRedirect(reverse('polls:question-detail', args=(3,)))
        else:
            context['message'] = 'Kody nie są identyczne'
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