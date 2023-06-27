from django.shortcuts import render, redirect, get_object_or_404
from ..models import Question, Answer
from ..forms import  AnswerForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone


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
