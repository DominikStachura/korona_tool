from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.detail import DetailView
import csv

from .models import Question, History
from django.urls import reverse


# class QuestionDetailView(DetailView):
#     model = Question
#     template_name = 'question_detail.html'
#
#     def get_object(self, *args, **kwargs):
#         request = self.request
#         pk = self.kwargs.get('pk')
#         instance = get_object_or_404(Question, pk=pk)
#         print(len(list(instance.choice_set.all())))
#
#
#
#         return instance

def question_view(request, pk=None):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('home'))
    else:
        history_instance = History.objects.all().filter(assigned_user=request.user).first()
        questions_history = history_instance.questions_all
        answers_history = history_instance.answers_all
        # print(request.user.is_authenticated)
        question = Question.objects.filter(pk=pk).first()
        # print(question.choice_set.all())
        numerical = False
        if len(list(question.choice_set.all())) == 0:
            numerical = True
        context = {'question': question,
                   'numerical': numerical}

        questions_history = f'{questions_history}||{question.question_text}'
        if request.method == 'POST':
            if numerical:
                value = request.POST.get('value')
                question.numerical_value = value
                question.save()
                answers_history = f'{answers_history}||{value}'
                history_instance.questions_all = questions_history
                history_instance.answers_all = answers_history
                history_instance.save()
                if question.next_question is None:
                    logout(request)
                    return HttpResponseRedirect(reverse('polls:final'))
                else:
                    next_question_id = question.next_question.id
                    return HttpResponseRedirect(reverse('polls:question-detail', args=(next_question_id,)))
            else:
                selected_choice = question.choice_set.get(pk=request.POST.get('choice'))
                answers_history = f'{answers_history}||{selected_choice.choice_text}'
                history_instance.questions_all = questions_history
                history_instance.answers_all = answers_history
                history_instance.save()
                if not (selected_choice.final):
                    if len(list(selected_choice.choiceorder_set.all().values())) > 0:
                        next_question_id = list(selected_choice.choiceorder_set.all().values())[0]['question_id']
                        return HttpResponseRedirect(reverse('polls:question-detail', args=(next_question_id,)))
                else:
                    logout(request)
                    return HttpResponseRedirect(reverse('polls:final'))

        return render(request, 'question_detail.html', context)


def output_view(request):
    context = {}
    if request.method == 'POST':
        code = request.POST.get('code')
        history = History.objects.all().filter(code=code)
        if history.exists() and history.first().answers_all is not None:
            history_instance = history.first()
            with open('output.csv', 'w') as f:
                writer = csv.writer(f)
                writer.writerows(
                    zip(history_instance.questions_all.split('||')[1:], history_instance.answers_all.split('||')[1:]))
            context['message'] = "Utworzono plik 'output.csv' "
        else:
            context['message'] = 'Brak danych przypisanych do danego kodu'
    return render(request, 'output.html', context)
