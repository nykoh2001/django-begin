from django.contrib import admin

# Register your models here.
from .models import Question, Answer

admin.site.register(Question, Answer)