from django.shortcuts import render, redirect

import requests
from django.conf import settings
# BeautifulSoup
from bs4 import BeautifulSoup

from magaObtain.article import Article
from magaObtain.articleList import ArticleList

from datetime import datetime
from dateutil.relativedelta import relativedelta


def index(request):
    url = f"https://katsumaweb.gio.filsp.jp/bn?ssid={settings.SSID}"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    if soup.find("div", {"id": "title2"}) and "ログイン画面" in soup.find("div", {"id": "title2"}).get_text():
        content = "サイトにログインし、SSIDを設定してください。"
    else:
        content = "ログインしました。"

    return render(request, 'index.html', {'content': content})


def list(request):
    atcList = ArticleList()
    atcList.readAll()
    lst = atcList.getListPerYearMonth()
    title = atcList.getTitle()

    return render(request, 'list.html', {"title": title, "list": lst})


def fetch(request):
    # 100記事分取得
    dt_now = datetime.now()
    curr_date = dt_now
    cnt = 0
    while cnt <= 100:
        atc = Article(curr_date.year, curr_date.month, curr_date.day)
        if atc.findByYMD():
            pass
        else:
            try:
                atc.fetch()
            except ValueError as e:
                print(e)
                return render(request, 'index.html', {'content': "サイトにログインし、SSIDを設定してください。"})
            atc.save()
            cnt += 1
        # 前の日
        curr_date = curr_date + relativedelta(days=-1)
    # リストを再表示
    return redirect(index)


def current(request):
    atc = Article("", "", "")
    if atc.findByYMD():
        atc.read()
    else:
        try:
            atc.fetch()
        except ValueError as e:
            print(e)
            return render(request, 'index.html', {'content': "サイトにログインし、SSIDを設定してください。"})
        atc.save()
    rtnContents = atc.getDisplayableContents()

    return render(request, 'article.html', {"data": {"subject": atc.getSubject(), "contents": rtnContents}})


def article(request, year, month, day):
    atc = Article(year, month, day)
    if atc.findByYMD():
        atc.read()
    else:
        try:
            atc.fetch()
        except ValueError as e:
            print(e)
            return render(request, 'index.html', {'content': "サイトにログインし、SSIDを設定してください。"})
        atc.save()
    rtnContents = atc.getDisplayableContents()

    return render(request, 'article.html', {"data": {"subject": atc.getSubject(), "contents": rtnContents}})


def search(request):
    if request.POST.get('searchQuery'):
        searchQuery = request.POST.get('searchQuery')
        if searchQuery != '':
            # 検索
            atcList = ArticleList()
            lst = atcList.search(searchQuery)
            data = {'searchQuery': searchQuery, 'list': lst}
        else:
            data = {'searchQuery': searchQuery}
    else:
        data = {'searchQuery': ''}
    return render(request, 'search.html', {'data': data})
