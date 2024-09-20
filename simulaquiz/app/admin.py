from django.contrib import admin
from .models import *

admin.site.register(Theme) #materia
admin.site.register(Exam) #assunto
admin.site.register(Question) #questoes
admin.site.register(Choices) #alternativas
admin.site.register(Moderator) #admin
#admin.site.register(SubmittedAnswer) #questões