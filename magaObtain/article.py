import requests
from django.conf import settings
from datetime import datetime
# BeautifulSoup
from bs4 import BeautifulSoup, re
# forms
from magaObtain.forms import ArticleForm
# models
from magaObtain.models import Article as mdlArticle


class Article():
    '''
    classdocs
    '''

    def __init__(self, year, month, day):
        '''
        Constructor
        '''
        self.__subject = ""
        self.__contents = []

        # 空欄の場合に現在年月日を補う
        dt_now = datetime.now()
        if year == "":
            self.__year = dt_now.year
        else:
            self.__year = year
        if month == "":
            self.__month = dt_now.month
        else:
            self.__month = month
        if day == "":
            self.__day = dt_now.day
        else:
            self.__day = day

    def read(self):
        """
        フィールドの日付の記事をDBから取得する
        """
        article = mdlArticle.objects.get(
            content_date=f"{self.__year}-{self.__month}-{self.__day}"
        )
        if article:
            # soup = BeautifulSoup(self.__contents)
            self.__subject = article.subject
            soup = BeautifulSoup(article.content, "html.parser")
            self.__contents = soup.find("div", {"id": "backnumber"})
            # self.__contents = article.content
        else:
            print(f"there is no article!!! content_date={self.__year}-{self.__month}-{self.__day}")
            self.__subject = ""
            self.__contents = []

    def fetch(self):
        """
        フィールドの日付の記事をサイトから取得する
        """

        url = f"https://katsumaweb.gio.filsp.jp/bn?year={self.__year}&month={self.__month}&day={self.__day}&write=on&ssid={settings.SSID}"
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        if soup.find("div", {"id": "title2"}) and "ログイン画面" in soup.find("div", {"id": "title2"}).get_text():
            raise ValueError("ログインしていません")

        if soup.find("div", {"id": "subject"}):
            self.__subject = soup.find("div", {"id": "subject"}).get_text()

        if soup.find("div", {"id": "backnumber"}):
            self.__contents = soup.find("div", {"id": "backnumber"})

        print("fetched: subject="+self.__subject)

    def getDisplayableContents(self):
        rtnContents = []
        if len(self.__contents) > 0:
            for child in self.__contents:
                if child.name != "br":
                    if child.name == "a":
                        rtnContents.append({"a": {"href": child['href'],"text": child.string}})
                    else:
                        if re.match(r'^・(.*)$', child.string):
                            rtnContents.append({"kadai": re.sub(r'^・', '', child.string)})
                        else:
                            rtnContents.append({"div": child.string})
        return rtnContents
    
    def getSubject(self):
        return self.__subject

    def findByYMD(self):
        if mdlArticle.objects.filter(content_date=f"{self.__year}-{self.__month}-{self.__day}").count() > 0 :
            return True
        else:
            return False

    def save(self):
        # 同日のスクレイピングが正常かつ同日のDBデータがないことを確認
        if self.__subject and self.findByYMD() is False:
            # データがない場合formを作成して保存
            form = ArticleForm({
                'content_date': f"{self.__year}-{self.__month}-{self.__day}",
                'subject': self.__subject,
                'content': self.__contents
            })

            if form.is_valid():
                mdl_article = form.save()
                mdl_article.save()
                print(f"saved!!! :content_date={self.__year}-{self.__month}-{self.__day} submect="+self.__subject)
            else:
                print(f"valid error:content_date={self.__year}-{self.__month}-{self.__day} submect="+self.__subject)
        else:
            print(f"didnt save:no site data yet or db data already exists. :content_date={self.__year}-{self.__month}-{self.__day}")