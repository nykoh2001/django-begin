from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.http import HttpResponseNotAllowed

# Create your views here.

from .models import Question, Answer
from .forms import QuestionForm, AnswerForm

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
  # answer = Answer(question=question, content = req.POST.get('content'), create_date = timezone.now())
  # answer.save()
  if req.method == "POST":
        form = AnswerForm(req.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('pybo:detail', question_id=question.id)
  else:
      return HttpResponseNotAllowed('Only POST is possible.')
  context = {'question': question, 'form': form}
  return render(req, 'pybo/question_detail.html', context)

def question_create(req):
  if req.method == "GET":
    form = QuestionForm()
    return render(req, 'pybo/question_form.html', {'form': form})
  if req.method=="POST":
    form = QuestionForm(req.POST)
    if form.is_valid():
      question = form.save(commit=False)
      question.create_date = timezone.now()
      question.save()
  return redirect("pybo:index")