from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

# Create your views here.

from .models import Question, Answer
from .forms import QuestionForm

def index(req):
  question_list = Question.objects.order_by('-create_date')
  context = {'question_list': question_list}
  return render(req, 'pybo/question_list.html', context)

def detail(req, question_id):
  question = get_object_or_404(Question, id=question_id)
  context = {'question': question}
  return render(req, 'pybo/question_detail.html', context)

def answer_create(req, question_id):
  question = get_object_or_404(Question, pk=question_id)
  # question.answer_set.create(content=req.POST.get('content'), create_date=timezone.now())
  answer = Answer(question=question, content = req.POST.get('content'), create_date = timezone.now())
  answer.save()
  return redirect('pybo:detail', question_id = question.id)

def question_create(req):
  form = QuestionForm()
  return render(req, 'pybo/question_form.html', {'form': form})