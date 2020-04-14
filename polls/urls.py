from django.urls import path
from django.views.generic import TemplateView
# from .views import QuestionDetailView
from .views import question_view, output_view, intro_view, return_view

app_name = 'polls'
urlpatterns = [
    path('intro_login', TemplateView.as_view(template_name='intro_login.html'), name='intro_login'),
    path('intro', intro_view, name='intro'),
    path('<int:pk>/', question_view, name='question-detail'),
    path('final', TemplateView.as_view(template_name='final.html'), name='final'),
    path('output', output_view, name='output'),
    path('return', return_view, name='return'),
]