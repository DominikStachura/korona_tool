from django.urls import path
from django.views.generic import TemplateView
# from .views import QuestionDetailView
from .views import question_view

app_name = 'polls'
urlpatterns = [
    # path('<int:pk>/', QuestionDetailView.as_view(), name='question-detail'),
    path('<int:pk>/', question_view, name='question-detail'),
    path('final', TemplateView.as_view(template_name='final.html'), name='final')
]