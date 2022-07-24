from django import forms
from magaObtain.models import Article as mdlArticle


class ArticleForm(forms.ModelForm):
    class Meta:
        model = mdlArticle
        fields = ('content_date', 'subject', 'content')
