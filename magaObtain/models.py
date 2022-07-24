from django.conf import settings
from django.db import models


class Article(models.Model):
    content_date = models.DateField('日付')
    subject = models.CharField('タイトル', max_length=128)
    content = models.TextField('内容')
    created = models.DateTimeField('取得日', auto_now_add=True)
    updated = models.DateTimeField('更新日', auto_now=True)

    def __str__(self):
        return self.content_date
