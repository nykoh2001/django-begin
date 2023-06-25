from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.http import HttpResponseNotAllowed
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.

from .models import Question, Answer
from .forms import QuestionForm, AnswerForm

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

@login_required(login_url="common:login")
def answer_create(req, question_id):
  question = get_object_or_404(Question, pk=question_id)
  # question.answer_set.create(content=req.POST.get('content'), create_date=timezone.now())
  # answer = Answer(question=question, content = req.POST.get('content'), create_date = timezone.now())
  # answer.save()
  if req.method == "POST":
        form = AnswerForm(req.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.author = req.user
            answer.create_date = timezone.now()
            answer.question = question
            answer.save()
            return redirect('pybo:detail', question_id=question.id)
  else:
      form = AnswerForm()
  context = {'question': question, 'form': form}
  return render(req, 'pybo/question_detail.html', context)

@login_required(login_url="common:login")
def question_create(req):
  if req.method == "GET":
    form = QuestionForm()
    return render(req, 'pybo/question_form.html', {'form': form})
  print("post")
  if req.method=="POST":
    form = QuestionForm(req.POST)
    if form.is_valid():
      question = form.save(commit=False)
      question.author = req.user
      question.create_date = timezone.now()
      question.save()
  return redirect("pybo:index")

@login_required(login_url='common:login')
def question_modify(request, question_id):
  question = get_object_or_404(Question,pk=question_id)
  if request.user != question.author:
    messages.error("수정 권한이 없습니다.")
    return redirect('pybo:detail', question_id=question_id)
  if request.method=="POST":
    form = QuestionForm(request.POST, instance=question)
    if form.is_valid():
      question = form.save(commit=False)
      question.modify_date = timezone.now()
      question.save()
      return redirect('pybo:detail', question_id =question_id)
  else:
    form = QuestionForm(instance=question)
  context = {'form': form}
  return render(request, 'pybo/question_form.html', context)
    
@login_required(login_url='common:login')  
def question_delete(request, question_id):
  question = get_object_or_404(Question, pk=question_id)
  if request.user != question.author:
    messages.error('삭제 권한이 없습니다.')
    return redirect('pybo:detail', question_id=question_id)
  question.delete()
  return redirect('pybo:index')
  
@login_required(login_url='common:login')
def answer_modify(request, answer_id):
  answer = get_object_or_404(Answer, pk=answer_id)
  if request.user != answer.author:
    messages.error("수정 권한이 없습니다.")
    return redirect('pybo:detail', question_id = answer.question.id)
  if request.method == "POST":
    form = AnswerForm(request.POST, instance=answer)
    if form.is_valid():
      answer= form.save(commit=False)
      answer.modify_date = timezone.now()
      answer.save()
      return redirect('pybo:detail', question_id = answer.question.id)
  else:
    form = AnswerForm(instance=answer)
  context= {'form': form}
  return render(request, 'pybo/answer_form.html', context)

@login_required(login_url='common:login')
def answer_delete(request, answer_id):
  answer = get_object_or_404(Answer, pk=answer_id)
  if request.user != answer.author:
    messages.error("삭제 권한이 없습니다.")
  else: answer.delete()
  return redirect('pybo:detail', question_id=answer.question.id)
