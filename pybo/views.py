from django.shortcuts import render, get_object_or_404

# Create your views here.

from .models import Question

def index(req):
  question_list = Question.objects.order_by('-create_date')
  context = {'question_list': question_list}
  return render(req, 'pybo/question_list.html', context)

def detail(req, question_id):
  question = get_object_or_404(Question, id=question_id)
  context = {'question': question}
  return render(req, 'pybo/question_detail.html', context)