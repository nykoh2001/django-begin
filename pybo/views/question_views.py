from django.utils import timezone
from django.shortcuts import render, get_object_or_404, redirect
from ..models import Question 
from ..forms import QuestionForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

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
def question_vote(request, question_id):
  question = get_object_or_404(Question, pk=question_id)
  if request.user == question.author:
    messages.error(request=request, message="본인이 작성한 글은 추천할 수 없습니다.")
  else:
    question.voter.add(request.user)
  return redirect('pybo:detail', question_id=question.id)