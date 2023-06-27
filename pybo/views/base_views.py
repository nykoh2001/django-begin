from ..models import Question
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404

def index(req):
  page = req.GET.get('page', 1)
  question_list = Question.objects.order_by('-create_date')
  paginator = Paginator(question_list, 10)
  page_object = paginator.get_page(page)
  context = {'question_list': page_object}
  return render(req, 'pybo/question_list.html', context)

def detail(req, question_id):
  question = get_object_or_404(Question, id=question_id)
  context = {'question': question}
  return render(req, 'pybo/question_detail.html', context)
