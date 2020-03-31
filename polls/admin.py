from django.contrib import admin

from .models import Choice, ChoiceOrder, Question, History


class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3


class OrderInline(admin.TabularInline):
    model = ChoiceOrder
    extra = 1



class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['question_text', 'next_question', 'numerical_value']}),
    ]
    inlines = [ChoiceInline]
    list_display = ['question_text', 'next_question', 'numerical_value']
    search_fields = ['question_text']

    class Meta:
        model = Question


class ChoiceAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['choice_text', 'final']}),
    ]
    list_display = ['choice_text', 'question', 'final']
    inlines = [OrderInline]

    class Meta:
        model = Choice

class HistoryAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'pub_date']
    class Meta:
        model = History


admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice, ChoiceAdmin)
admin.site.register(History, HistoryAdmin)
