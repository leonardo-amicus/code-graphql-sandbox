from django.db import models
from datetime import datetime


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    edit_date = models.DateTimeField(default=datetime.now())


class Response(models.Model):
    response_text = models.CharField(max_length=200)
    create_date = models.DateTimeField(auto_now_add=True)
    edit_date = models.DateTimeField(default=datetime.now())
    question = models.ForeignKey(Question,
                                 on_delete=models.CASCADE,
                                 related_name='responses')
