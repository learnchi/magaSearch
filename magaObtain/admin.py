from django.contrib import admin

# Register your models here.
from magaObtain.models import Article

# 以下の記載で/adminからテーブルデータ操作可能になる
admin.site.register(Article)
# python manage.py createsuperuser で管理ユーザーが追加できる