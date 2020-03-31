from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.detail import DetailView
from korona.utils import get_download_path
import csv
import xlsxwriter

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
                    # return HttpResponseRedirect(reverse('polls:final'))
                    context['code'] = request.user.username
                    logout(request)
                    return render(request, 'final.html', context)
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
                    # return HttpResponseRedirect(reverse('polls:final'))
                    context['code'] = request.user.username
                    return render(request, 'final.html', context)

        return render(request, 'question_detail.html', context)


def output_view(request):
    context = {}
    if request.method == 'POST':
        code = request.POST.get('code')
        history = History.objects.all().filter(code=code)
        if history.exists():
            download_path = get_download_path()
            workbook = xlsxwriter.Workbook(f'{download_path}/output.xlsx')
            for index, history_instance in enumerate(history):
                # history_instance = history.first()
                if history_instance.answers_all is not None:
                    # file_name = f'output_{history_instance.pub_date.strftime("%Y%m%d-%H%M%S")}.csv'
                    # with open(file_name, 'w') as f:
                    #     writer = csv.writer(f)
                    #     writer.writerows(
                    #         zip(history_instance.questions_all.split('||')[1:], history_instance.answers_all.split('||')[1:]))
                    row = 0
                    col = 0
                    worksheet = workbook.add_worksheet(f'{history_instance.pub_date.strftime("%Y%m%d-%H%M%S")}')
                    for q, a in zip(history_instance.questions_all.split('||')[1:], history_instance.answers_all.split('||')[1:]):
                        worksheet.write(row, col, q)
                        worksheet.write(row, col + 1, a)
                        row += 1
            workbook.close()




            context['message'] = "Zapisano dane to folderu 'pobrane' "
        else:
            context['message'] = 'Brak danych przypisanych do danego kodu'
    return render(request, 'output.html', context)
