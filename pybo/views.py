from django.shortcuts import render

# Create your views here.

from .models import Question

def index(req):
  question_list = Question.objects.order_by('-create_date')
  context = {'question_list': question_list}
  return render(req, 'pybo/question_list.html', context)

def detail(req, question_id):
  question = Question.objects.get(id=question_id)
  context = {'question': question}
  return render(req, 'pybo/question_detail.html', context)