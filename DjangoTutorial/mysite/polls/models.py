from django.db import models
from django.utils import timezone

import datetime


# Create your models here.
class Question(models.Model):
    question_text = models.CharField(max_length=200)
    # 这里的data published是在后台显示的名称
    pub_date = models.DateTimeField('data published')

    # 这个str函数的作用，是执行python manage.py shell 的时候 输入Question.objects.all()可以看到具体的细节
    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        return timezone.now() - datetime.timedelta(days=1) <= self.pub_date <= timezone.now()


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
