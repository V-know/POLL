from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Question(models.Model):
    author_name = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='作者')
    question_text = models.CharField(max_length=200)
    ready = models.IntegerField(default=0)  # 管理员审核  如果可以，ready 加 1 。显示在投票系统中。
    created_datetime = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    end_date = models.DateTimeField(null=True, blank=True, verbose_name='结束日期')
    objects = None

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
