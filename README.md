# メルマガ検索＆リーダー MagaSearch

勝間和代氏のサポートメール内容を蓄積しつつ全文検索するツールです。

勝間和代氏のサポートメールを購読している必要があります。

# 動作環境

Python、Djangoが動作する環境が必要です。

ローカルホストで動かすことを想定しています。

# 導入方法

プロジェクトを取得します。

`manage.py`のあるディレクトリから、データベースの設定をします。
コンソールを開き、manage.pyのあるディレクトリに移動してから、
`python manage.py makemigrations'と入力してください。


実行例

```
C:\magaSearch>python manage.py makemigrations
System check identified some issues:

Migrations for 'magaObtain':
  magaObtain\migrations\0001_initial.py
    - Create model Article

C:\magaSearch>python manage.py migrate
System check identified some issues:

Operations to perform:
  Apply all migrations: admin, auth, contenttypes, magaObtain, sessions
Running migrations:
  Applying magaObtain.0001_initial... OK
```

# 動かし方

コンソールを開き、manage.pyのあるディレクトリに移動してから、
`python manage.py runserver'と入力してください。


```
C:\magaSearch>python manage.py runserver
Watching for file changes with StatReloader
Performing system checks...

System check identified some issues:

System check identified 1 issue (0 silenced).
September 23, 2022 - 17:00:26
Django version 4.1.1, using settings 'magaSearch.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

ブラウザから`http://localhost:8000/`を表示します。
「サイトにログインし、SSIDを設定してください。」
と表示できたら成功です。

# メールマガジンとの連携

サポートメールのバックナンバーURLにアクセスし、ログインします。
ブラウザのURL部分から、`SSID=XXXX`部分をコピーします。
32桁の英数字のようです。

この部分を/magaSearch/magaSearch/settings.py のいちばん最後の行にある、
`SSID = 'xxxxxxxxxx'` のxxx部分と置き換えます。

もう一度ブラウザから`http://localhost:8000/`を表示します。
「ログインしました。」
と表示できたら成功です。

# メールマガジンの取得

左のメニューからlistをクリックします。
「サイトから100記事分取得」をクリックします。
しばらくすると、新しい順に取得した記事の一覧が表示されます。
取得した記事のタイトルがrunserverを実行したコンソールにも表示されます。
繰り返し押すと、過去にさかのぼり100記事ずつ取得します。

# 記事の見方

listから読みたい記事のタイトルをクリックすると、記事の内容が表示されます。

# 検索

左のメニューから「search」をクリックします。
文字入力ウインドウに検索したい文字を入れて検索キーをクリックします。
取得した記事を検索し、該当する記事のタイトルと本文の一部が表示されます。
読みたい記事のタイトルをクリックすると、記事の内容が表示されます。

