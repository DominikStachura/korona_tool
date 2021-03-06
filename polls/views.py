from django.contrib.auth import logout
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse

from korona.utils import create_spreadsheet_data
from .models import Question, History

def update_session(request):
    url_list = request.session.get('urls_history')
    if url_list is None:
        request.session['urls_history'] = request.path
    else:
        url_list.append(request.path)
        request.session['urls_history'] = url_list

def question_view(request, pk=None):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('home'))
    else:
        # request.session['urls_history'].append(request.path)


        history_instance = History.objects.all().filter(assigned_user=request.user).order_by('-id')[0]
        questions_history = history_instance.questions_all
        answers_history = history_instance.answers_all
        # print(request.user.is_authenticated)
        question = Question.objects.filter(pk=pk).first()
        # print(question.choice_set.all())
        numerical = False
        if len(list(question.choice_set.all())) == 0:
            numerical = True
        context = {'question': question,
                   'numerical': numerical,
                   'code': request.user.username}

        questions_history = f'{questions_history}||{question.question_text}'
        if request.method == 'POST':
            update_session(request)

            if numerical:
                value = request.POST.get('value')
                answers_history = f'{answers_history}||{value}'
                history_instance.questions_all = questions_history
                history_instance.answers_all = answers_history
                history_instance.save()
                if question.next_question is None:
                    # return HttpResponseRedirect(reverse('polls:final'))
                    logout(request)
                    return render(request, 'final.html', context)
                else:
                    next_question_id = question.next_question.id
                    # return HttpResponseRedirect(reverse('polls:question-detail', args=(next_question_id,)))
                    return redirect(reverse('polls:question-detail', args=(next_question_id,)))
            else:
                selected_choice = question.choice_set.get(pk=request.POST.get('choice'))
                answers_history = f'{answers_history}||{selected_choice.choice_text}'
                history_instance.questions_all = questions_history
                history_instance.answers_all = answers_history
                history_instance.save()
                if not (selected_choice.final):
                    if len(list(selected_choice.choiceorder_set.all().values())) > 0:
                        next_question_id = list(selected_choice.choiceorder_set.all().values())[0]['question_id']
                        # return HttpResponseRedirect(reverse('polls:question-detail', args=(next_question_id,)))
                        return redirect(reverse('polls:question-detail', args=(next_question_id,)))
                else:
                    logout(request)
                    # return HttpResponseRedirect(reverse('polls:final'))
                    return render(request, 'final.html', context)

        return render(request, 'question_detail.html', context)


def output_view(request):
    context = {}
    if request.method == 'POST':
        code = request.POST.get('code')
        data = create_spreadsheet_data(code=code)

        if data is not None:
            response = HttpResponse(data,
                                    content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename="output' + code + '.xlsx"'
            return response
        else:
            context['message'] = 'Brak danych przypisanych do danego kodu'
    return render(request, 'output.html', context)


def intro_view(request):
    request.session['urls_history'] = [request.path]
    context = {}
    context['code'] = request.user.username
    if request.method == 'POST':
        return HttpResponseRedirect(reverse('polls:question-detail', args=(3,)))
    else:
        return render(request, 'intro.html', context)


def return_view(request):
    urls = request.session['urls_history']
    prev_url = urls[-1]
    if 'intro' in prev_url.split('/')[-1]:
        return redirect(request.META.get('HTTP_REFERER'))

    history_instance = History.objects.all().filter(assigned_user=request.user).order_by('-id')[0]
    history_instance.answers_all = '||'.join(history_instance.answers_all.split('||')[:-1])
    history_instance.questions_all = '||'.join(history_instance.questions_all.split('||')[:-1])
    history_instance.save()
    urls = request.session['urls_history']
    prev_url = urls[-1]
    request.session['urls_history'] = urls[:-1]
    return redirect(prev_url)