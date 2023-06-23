from django.contrib.auth import login, authenticate
from .forms import UserForm
from django.shortcuts import render, redirect

def signup(req):
  if req.method == "POST":
    form = UserForm(req.POST)
    if form.is_valid():
      form.save()
      username = form.cleaned_data.get('username')
      raw_password = form.cleaned_data.get('password1')
      user = authenticate(username=username, password=raw_password)
      login(req, user)
      redirect("index")
  else:
    form = UserForm()
  return render(req, 'common/signup.html', {'form': form})

      