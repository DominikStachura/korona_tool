from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views.generic.detail import DetailView

from .models import Question
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
    question = Question.objects.filter(pk=pk).first()
    # print(question.choice_set.all())
    numerical = False
    if len(list(question.choice_set.all())) == 0:
        numerical = True
    context = {'question': question,
               'numerical': numerical}

    if request.method == 'POST':
        if numerical:
            value = request.POST.get('value')
            question.numerical_value = value
            question.save()
            if question.next_question is None:
                return HttpResponseRedirect(reverse('polls:final'))
            else:
                next_question_id = question.next_question.id
                return HttpResponseRedirect(reverse('polls:question-detail', args=(next_question_id,)))
        else:
            selected_choice = question.choice_set.get(pk=request.POST.get('choice'))
            if not(selected_choice.final):
                if len(list(selected_choice.choiceorder_set.all().values())) > 0:
                    next_question_id = list(selected_choice.choiceorder_set.all().values())[0]['question_id']
                    return HttpResponseRedirect(reverse('polls:question-detail', args=(next_question_id,)))
            else:
                return HttpResponseRedirect(reverse('polls:final'))

    return render(request, 'question_detail.html', context)
