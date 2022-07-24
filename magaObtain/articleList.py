# models
from magaObtain.models import Article as mdlArticle
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import re  # 正規表現
from django.db.models import Q


class ArticleList():
    '''
    classdocs
    '''

    def __init__(self, year="", month="", day=""):
        '''
        Constructor
        '''
        self.__title = ""
        self.__list = {}

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

        # self.__title=str(self.__year)+"年"+str(self.__month)+"月"
        self.__title = "リスト"

    def readAll(self):
        self.__list = mdlArticle.objects.order_by("-content_date")

    def readListPerMonth(self):

        # 今月の1日
        dt_start = date(self.__year, self.__month, 1)
        # 今月の末日
        # dt_end = dt_start + relativedelta(months=+1,day=1,days=-1)
        dt_end = dt_start + relativedelta(months=+1, day=1)

        # LIST取得
        self.__list = mdlArticle.objects.filter(content_date__gte=dt_start).filter(content_date__lt=dt_end).order_by("-content_date")

    def readListPerYear(self):
        # フィールドの年の1月1日
        dt_start = date(self.__year, 1, 1)
        # フィールド翌年の1月1日
        dt_end = dt_start + relativedelta(year=+1)
        # LIST取得
        self.__list = mdlArticle.objects.filter(content_date__gte=dt_start).filter(content_date__lt=dt_end).order_by("-content_date")

    def getList(self):
        return self.__list

    def getTitle(self):
        return self.__title

    def getListPerYearMonth(self):
        """
        listを年月別に加工する
        """
        strYearMonth = ""
        retList = {}
        for val in self.__list:
            if strYearMonth == str(val.content_date.year)+"-"+str(val.content_date.month):
                retList[strYearMonth].append(val)
            else:
                strYearMonth = str(val.content_date.year)+"-"+str(val.content_date.month)
                retList[strYearMonth] = [val]
        return retList

    def search(self, searchQuery):
        self.__list = mdlArticle.objects.filter(
            Q(content__contains=searchQuery) | Q(subject__contains=searchQuery)
        ).order_by("-content_date")

        if self.__list:

            strYearMonth = ""
            retList = {}
            for val in self.__list:
                s = val.content
                m = re.search(searchQuery, s)
                if m:
                    val.content = val.content[m.start()-50:m.start()] + '<font color="red">' + m.group() + '</font>' + val.content[m.end():m.end()+50]
                s = val.subject
                m = re.search(searchQuery, s)
                if m:
                    val.subject = val.subject[:m.start()] + '<font color="red">' + m.group() + '</font>' + val.subject[m.end():]

                if strYearMonth == str(val.content_date.year)+"-"+str(val.content_date.month):
                    retList[strYearMonth].append(val)
                else:
                    strYearMonth = str(val.content_date.year)+"-"+str(val.content_date.month)
                    retList[strYearMonth] = [val]
            return retList
        return None
