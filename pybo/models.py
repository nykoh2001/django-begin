from django.db import models

# Create your models here.
class Question:
  subject = models.CharField(max_length=200)
  content = models.TextField()
  create_date = models.DateTimeField()
  
class Answer:
  question = models.ForeignKey(Question, on_delete=models.CASCADE)
  content = models.TextField()
  create_date = models.DateTimeField()
  

  