# DjangoでBlog作成

今回のアプリは「動かして学ぶ！Python Django開発入門」に沿ったものです。

詳細は本を読んでください。

本の中で環境設定部分はPyCharmでの設定になっており、PyCharmを使わないと初心者は出来上がらないことになります。VS-Codeなど他のエディタを使っても適切に環境設定する方法を学習することがねらいです。

AWSのデプロイはやりません。気が向いたらHEROKUにデプロイします。

## 設計

### 画面イメージ

簡単な画面イメージを作成します。



#### URLと完成イメージ

| 画面名           | URL（ホスト名以降）   |
| ---------------- | --------------------- |
| トップページ     | `/`                   |
| 問い合せページ   | `/inquiry/`           |
| ブログ一覧ページ | `/blog-list/`         |
| ブログ作成ページ | `/blog-create/`       |
| ブログ詳細ページ | `/blog-detail/<key>/` |
| ブログ編集ページ | `/blog-update/<key>/` |
| ブログ削除ページ | `/blog-delete/<key>/` |

## 仮想環境作成

Python仮想環境はvenvで作成します。

### pipのアップデート

`pip` は頻繁にアップデートされます。まず最初に最新版にアップデートしておきます。

Windowsはpip、Macは通常pip3を使います。今後Macの場合はpipをpip3に読み替えて使用してください。

`pip` アップデートコマンド

```
pip install --upgrade pip
```

仮想環境  `venv` 作成のためのコマンドは次の通りです。
コマンドを実行すると、Homeフォルダ内に指定したフォルダが出来上がり、その中に  `venv` で必要なフォルダやファイルがインストールされます。
Windows の場合は My Document にできます。

**今回の仮想環境はdj_mysqlとします。**

`venv` の仮想環境を作成するコマンド

```
python -m venv dj_blog
```

`cd`コマンドで出来上がったフォルダ（ここではvenv_sample）に移動して、仮想環境に入るには次のコマンドを実行します。

#### Macの場合

Macで`venv` の仮想環境を実行するコマンド

```
source bin/activate
```

#### Windowsの場合

Windowsの場合、パスの区切りはスラッシュではなくバックスラッシュ `\` または `￥` マークを使います。

Windowsで`venv` の仮想環境を実行するコマンド

```
Scripts\activate
```

#### Windowsで仮想環境を実行時に出るエラー対策

`Scripts\activate`で**「PSSecurityException」**が発生する場合があります。

この場合「今開いているPowerShellウィンドウのみ実行ポリシーを変更」にします。

この場合はPowerShellに管理者権限は必要なく次のコマンドを実行します。

```
Set-ExecutionPolicy RemoteSigned -Scope Process
```

実行ポリシーを聞かれますので、「Y」を入力

再び仮想環境に入ります。

```
Scripts\activate
```

仮想環境に入るとターミナルのカレントディレクトリの表示に仮想環境の表示が加わります。
これで仮想環境に入りましたので、開発に必要なライブラリなどのインストールを `pip` などで行います。

#### 仮想環境から出る

仮想環境から出るには次のコマンドを実行します。



仮想環境から出るコマンド

```
deactivate
```

## Djangoのインストール

Djangoのインストールは`pip` で行います。以下のコマンドでは最新のバーションがインストールされます。



Djangoインストールコマンド

```
pip install django
```

Djangoのバージョン確認は以下コマンドです。

**-mオプション**について：Pythonは-mオプションを付けてpythonを実行するとモジュールを実行してくれます。つまり、これを付けないと正しく実行されない場合があると言うことです。



Djangoのバージョン確認コマンド

```
python -m django --version
```

今回のバージョンは3.1が返ってきました。

#### Djangoのバージョンを指定してインストール

バージョンが変わると突然動かなくなるなどトラブルに見舞われることがあります。

動作確認がとれた特定のバージョンのものをインストールすることもできます。



バージョン指定したインストール方法

```
pip install django=[バージョン番号]
```

## PostgreSQLのインストール

PostgreSQLをデータベースにします。本番環境はHeroku としますので、Herokuの最新バージョンに合わせます。

現在（2020-09-21）のバージョンは[こちらのページ](https://devcenter.heroku.com/articles/heroku-postgresql#version-support-and-legacy-infrastructure)で確認できます。

> Heroku Postgresは、少なくとも3つのメジャーバージョンを同時にサポートします。現在サポートされているバージョンは次のとおりです。
>
> - 12 (default)
> - 11
> - 10
> - 9.6
> - 9.5 - deprecating

#### Windowsの場合

[PostgreSQLのサイトのダウンロードページ](https://www.enterprisedb.com/downloads/postgres-postgresql-downloads)からダウンロードします。



#### Macの場合

**いったん仮想環境から抜けてインストールします。**

Homebrewを使ったインストール。現在最新版が12なのでバージョン指定しないでインストール

```
brew install postgresql
```

バージョン指定する場合

```
brew install postgresql@12
```

エラーが出た場合

Error: The following directories are not writable by your user:

/usr/local/share/man/man8

You should change the ownership of these directories to your user.

 sudo chown -R $(whoami) /usr/local/share/man/man8

And make sure that your user has write permission.

 chmod u+w /usr/local/share/man/man8

この場合、表示された通りにします。要は書き込み権限がないと言われてます。

$(whoami)は自分のMACのユーザー名にします。パスワードを聞かれるのでMACのパスワードを入れます。

所有権をユーザーに変更します。

```
sudo chown -R tahara /usr/local/share/man/man8
```

ユーザーに書き込み権限を与えます。

```
 chmod u+w /usr/local/share/man/man8
```

もう一度`brew install postgresql`を実行します。

#### 参考：ファイル・ディレクトリの権限（パーミッション）

**chmodコマンド**を使います。

変更対象は以下のいずれかで表します。

| 変更対象 | 意味     |
| :------- | :------- |
| u        | ユーザー |
| g        | グループ |
| o        | その他   |
| a        | すべて   |

変更方法については以下のいずれかで表します。

| 変更方法 | 意味                   |
| :------- | :--------------------- |
| =        | 指定した権限にする     |
| +        | 指定した権限を付与する |
| -        | 指定した権限を除去する |

変更内容については以下のいずれかで表します。

| 変更内容 | 意味     |
| :------- | :------- |
| r        | 読み取り |
| w        | 書き込み |
| x        | 実行     |



### PostgreSQLのバージョンの確認

```
psql --version
```

UTF8でデータベース作成するには次の内容を設定します。

```
initdb /usr/local/var/postgres -E utf8
```

PostgreSQL起動

```
brew services start postgresql
```

PostgreSQL停止

```
brew services stop postgresql
```



アンインストール

```
brew services stop postgresql
brew uninstall postgresql
rm -r /usr/local/var/postgres
```

再起動

```
brew services restart postgresql
```

参考：https://note.com/kodokuna_dancer/n/n3379b7c7fc6e

#### 新規データベース作成

my_blogという新規データベースを作成します。

```
createdb my_blog
```

データベース一覧確認

```
psql -l
```

**ここで仮想環境に戻ります。**

念のため仮想環境からデータベース一覧を確認します。

```
psql -l
```

### PostgreSQL接続ドライバ導入

PostgrSQLにpythonから接続するためのpsycopg2をインストール

```
pip install psycopg2-binary
```

ここでPostgrSQLを停止するには次のコマンド

```
brew services stop postgresql
```



## Djangoプロジェクトの作成

仮想環境dj_blogにカレントディレクトリを移動しておきます。また仮想環境にactivateしておきます。

次に、BLOGフォルダを作成します。できたらcdコマンドでカレントディレクトリをBLOGに移動します。

```
　cd BLOG
```



コマンドでDjangoプロジェクトを作成します。プロジェクト名はblogとします。

```
django-admin startproject blog .
```

treeコマンドでblogのフォルダとファイルの構成を確認

```
tree
```

zsh: command not found: treeとなった場合、zshにはtreeコマンドが無いのでインストールします。

```
brew install tree
```

もう一度

```
tree
```

treeコマンドの結果

```
.
├── blog
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
└── manage.py
```



## Djangoアプリケーションの作成

現在の階層からアプリケーションを作成します。

```
python manage.py startapp my_blog
```

アプリケーションフォルダmy_blogが作成されます。

treeコマンドの結果

```
.
├── blog
│   ├── __init__.py
│   ├── __pycache__
│   │   ├── __init__.cpython-38.pyc
│   │   └── settings.cpython-38.pyc
│   ├── asgi.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── manage.py
└── my_blog
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── migrations
    │   └── __init__.py
    ├── models.py
    ├── tests.py
    └── views.py
```

### settings.pyの編集

INSTALLED_APPSに`'my_blog.apps.MyBlogConfig'`を追加。

この内容はアプリの名前次第で変わります。app.pyで自動作成された `class MyBlogConfig(AppConfig):` と
    ` name = 'my_blog'` の名前をよく確認して編集してください。

blog/settings.py

```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'my_blog.apps.MyBlogConfig',
]
```

my_blog/apps.py

この内容は自動でできています。

```
from django.apps import AppConfig


class MyBlogConfig(AppConfig):
    name = 'my_blog'
```

#### タイムゾーンの変更

言語とタイムゾーンを日本仕様に変更します。

blog/settings.py

```
LANGUAGE_CODE = 'ja'

TIME_ZONE = 'Asia/Tokyo'
```

### データベースの設定

デフォルトのSQLite3の設定からPostgreSQLに変更します。

'NAME': 'my_blog'はデータベース名で最初に新規作成したデータベース名を入れます。

ユーザー名とパスワードはデータベースを作成したユーザー名とパスワードになります。

**GitHubなど使う場合は必ず重要な情報は環境変数を使います。**

MACの場合はデフォルトのスーパーユーザー`''`、パスワードも`''`で無しの設定を環境変数に設定します。

何らかユーザー設定とパスワードを設定した場合はその値を環境変数に設定します。

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'my_blog',
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': '',
        'PORT': '',
    }
}
```

### 環境変数の設定

最新のMACではzshがシェルに使われています。

ユーザーの環境変数はHOMEフォルダの直下に「.zshc」のファイルがあります。これが環境変数の設定ファイルです。BASHを使っている場合は「.bash_profile」です。新しいマシンの場合には設定ファイルが無い場合があります。そのときは自分で作ります。

また、先頭にドットがあるファイル名は特別なもので不可視ファイルと言われるものです。マシンのデフォルト状態では確認することができません。[不可視ファイルを見えるような設定](https://itstudio.co/2014/10/29/3218/)をしておきます。

git 「.zshc」のファイルに次の記述を追加します。何らかユーザーやパスワードを設定した場合はその値を入れます。

```
export 'DB_USER'=''
export 'DB_PASSWORD'=''
```

環境変数に SECRET_KEY も追加しておきます。(この値はダミーです)

```
export 'SECRET_KEY'='c(x+=6)_0+d7cm!$14$g-m$$xsocd)om(2&i2-&=sss9%bb+aaa'
```

settings.py の方も変更します。

settings.py

```
SECRET_KEY = os.environ['SECRET_KEY']
```



### ロギングの設定

ロギングの設定はログの出力設定を行うものです。特に何も設定しなくても最低限のログは出力されますが、開発用としてログの出力設定に指定あります。

ログレベル

| ログレベル | 用途                             |
| ---------- | -------------------------------- |
| DEBUG      | 開発時のデバッグ                 |
| INFO       | 正常処理の記録                   |
| WARNING    | 想定外処理の記録                 |
| ERROR      | CRITICALほどでないエラーの記録用 |
| CRITICAL   | システムダウンクラスの最大問題用 |

ロギングの設定はsetting.pyの最後に追記します。

Djangoのログとmy_blogのログのための設定です。

```
# ロギング設定
LOGGING = {
    'version': 1,  # 1固定
    'disable_existing_loggers': False,

    # ロガーの設定
    'loggers': {
        # Djangoが利用するロガー
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        # my_blogアプリケーションが利用するロガー
        'my_blog': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },

    # ハンドラの設定DEBUG指定
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'dev'
        },
    },

    # フォーマッタの設定
    'formatters': {
        'dev': {
            'format': '\t'.join([
                '%(asctime)s',
                '[%(levelname)s]',
                '%(pathname)s(Line:%(lineno)d)',
                '%(message)s'
            ])
        },
    }
}


```

### ルーティングの設定

settings.pyのROOT_URLCONFはプロジェクト名、つまりsettings.pyが入っているフォルダ名を指定します。

settings.py

```
ROOT_URLCONF = 'blog.urls'
```



ルーティングにはプロジェクト用とアプリ用があります。

プロジェクトのルーティング

blog/urls.py

```
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('my_blog.urls')),
]
```

アプリケーションのルーティング

こちらのファイルは自動で作成されないので自分で作成します。

my_blog/urls.py

```
from django.urls import path

from . import views


app_name = 'my_blog'
urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
]
```

### views.py



```
from django.shortcuts import render
from django.views import generic


class IndexView(generic.TemplateView):
    template_name = "index.html"
```

### テンプレート作成

templatesフォルダーをmy_blogアプリフォルダ内に作成

その中にindex.htmlを作成します。

my_blog/tamplates/index.html

```
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Document</title>
</head>
<body>
  <h1>Hello World!</h1>
</body>
</html>
```

### 開発サーバーの起動

PostgreSQL起動を行う。

```
brew services start postgresql
```

開発サーバーを起動します。

```
python manage.py runserver
```

## HOMEページの作りこみ

### 静的ファイルの設置

settings.pyに静的ファイルの場所を指定します。`STATIC_URL = '/static/'`の後に次の内容を追記します。

```
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)
```

### One Page Wonderテンプレートを使用

[One Page Wonder](https://startbootstrap.com/themes/one-page-wonder/)からダウンロードして、static フォルダに img フォルダと vendor フォルダを入れます。

### base.htmlの作成

templatesフォルダに各ページ共通で使えるbase.htmlを作成します。

#### staticの使い方

テンプレートで{% load static %}を定義してから{static}タグを使う

例

```
{% load static %}
<link rel="stylesheet" type="text/css" href="{% static 'css/mystyle.css' %}">
```

ブラウザに表示されるコード

```
<link rel="stylesheet" type="text/css" href="/static/css/mystyle.css">
```



#### titleタグ

titleはSEO上重要なタグになります。各ページごとにその内容は変更しなければなりません。

従ってここには　ブロックを埋め込みます。

```
<title>{% block title %}{% endblock %}</title>
```

各のページにはその内容を記述します。例えば index.html のtitle要素では次のように記述します。

```
{% extends 'base.html' %}

{% block title %}Web上にあなた専用の日記ページを保存できるサービス | Private Diary{% endblock %}
```



base.html

```
{% load static %}

<html lang="ja">

  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
    <meta name="description" content="">
    <meta name="author" content="">

    <title>{% block title %}{% endblock %}</title>

    <!-- Bootstrap core CSS -->
    <link href="{% static 'vendor/bootstrap/css/bootstrap.min.css' %}" rel="stylesheet">

    <!-- Custom fonts for this template -->
    <link href="https://fonts.googleapis.com/css?family=Catamaran:100,200,300,400,500,600,700,800,900" rel="stylesheet">
    <link href="https://fonts.googleapis.com/css?family=Lato:100,100i,300,300i,400,400i,700,700i,900,900i" rel="stylesheet">

    <!-- Custom styles for this template -->
    <link href="{% static 'css/one-page-wonder.min.css' %}" rel="stylesheet">

    <!-- My style -->
    <link rel="stylesheet" type="text/css" href="{% static 'css/mystyle.css' %}">
    {% block head %}{% endblock %}
  </head>

  <body>
	<div id="wrapper">
        <!-- Navigation -->
        <nav class="navbar navbar-expand-lg navbar-dark navbar-custom fixed-top">
          <div class="container">
            <a class="navbar-brand" href="{% url 'my_blog:index' %}">My Blog</a>
            <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarResponsive" aria-controls="navbarResponsive" aria-expanded="false" aria-label="Toggle navigation">
              <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarResponsive">
              <ul class="navbar-nav mr-auto">
                <li class="nav-item {% block active_inquiry %}{% endblock %}">
                  <a class="nav-link" href="#">INQUIRY</a>
                </li>
              </ul>
              <ul class="navbar-nav ml-auto">
                <li class="nav-item">
                  <a class="nav-link" href="#">Sign Up</a>
                </li>
                <li class="nav-item">
                  <a class="nav-link" href="#">Log In</a>
                </li>
              </ul>
            </div>
          </div>
        </nav>

        {% block header%}{% endblock %}

        {% block contents%}{% endblock %}

        <!-- Footer -->
        <footer class="py-5 bg-black">
          <div class="container">
            <p class="m-0 text-center text-white small">Copyright &copy; Private Dairy 2019</p>
          </div>
          <!-- /.container -->
        </footer>

        <!-- Bootstrap core JavaScript -->
        <script src="{% static 'vendor/jquery/jquery.min.js' %}"></script>
        <script src="{% static 'vendor/bootstrap/js/bootstrap.bundle.min.js' %}"></script>
  	</div>
  </body>

</html>
```



### CSSの追加

staticフォルダはBLOGフォルダ内に作成します。さらにcssフォルダを作成してその中にmystyl.cssファイルを作成

static/css/mystyle.css

```
body, #wrapper {
    display: flex;
    flex-direction: column;
    min-height: 100vh;
}

footer {
    margin-top: auto;
}
```

### index.html作成

次にindex.htmlを作成します。

```
{% extends 'base.html' %}
{% load static %}

{% block title %}Web上にあなた専用の日記ページを保存できるサービス | Private Diary{% endblock %}

{% block header%}
<header class="masthead text-center text-white">
  <div class="masthead-content">
    <div class="container">
      <h1 class="masthead-heading mb-0">Private Diary</h1>
      <h2 class="masthead-subheading mb-0">あなた専用の日記保存サービス</h2>
      <a href="#" class="btn btn-primary btn-xl rounded-pill mt-5">LOG IN</a>
    </div>
  </div>
  <div class="bg-circle-1 bg-circle"></div>
  <div class="bg-circle-2 bg-circle"></div>
  <div class="bg-circle-3 bg-circle"></div>
  <div class="bg-circle-4 bg-circle"></div>
</header>
{% endblock %}

{% block contents %}
<section>
  <div class="container">
    <div class="row align-items-center">
      <div class="col-lg-6 order-lg-2">
        <div class="p-5">
          <img class="img-fluid rounded-circle" src="{% static 'img/01.jpg' %}" alt="">
        </div>
      </div>
      <div class="col-lg-6 order-lg-1">
        <div class="p-5">
          <h2 class="display-4">Web Diary</h2>
          <p>Web上で作成/編集/削除ができる日記</p>
        </div>
      </div>
    </div>
  </div>
</section>

<section>
  <div class="container">
    <div class="row align-items-center">
      <div class="col-lg-6">
        <div class="p-5">
          <img class="img-fluid rounded-circle" src="{% static 'img/02.jpg' %}" alt="">
        </div>
      </div>
      <div class="col-lg-6">
        <div class="p-5">
          <h2 class="display-4">Save Your Diary</h2>
          <p>あなたの日記をWebに保存</p>
        </div>
      </div>
    </div>
  </div>
</section>

<section>
  <div class="container">
    <div class="row align-items-center">
      <div class="col-lg-6 order-lg-2">
        <div class="p-5">
          <img class="img-fluid rounded-circle" src="{% static 'img/03.jpg' %}" alt="">
        </div>
      </div>
      <div class="col-lg-6 order-lg-1">
        <div class="p-5">
          <h2 class="display-4">Membership System</h2>
          <p>会員制のWeb日記サービス</p>
        </div>
      </div>
    </div>
  </div>
</section>
{% endblock %}
```

ここでトップページを確認するとテンプレートが適用されて綺麗なページになっています。



## 問い合わせページ作成

* ルーティング
* ビューの追加
* フォームの定義
* テンプレート作成
* CSSでデザイン

### ルーティング

問い合わせページのルーティングは`my_blog` フォルダ内のurls.pyで作成します。

`path('inquiry', views.inquiryView.as_view(), name='inquiry')`をurlpatternsに追加します。

my_blog/urls.py

```
from django.urls import path

from . import views


app_name = 'my_blog'
urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
    path('inquiry', views.inquiryView.as_view(), name='inquiry')
]
```

### views.pyの追加

urlsで `views.inquiryView` を記述したわけですから、views.pyで `inquiryView` を定義する必要があります。

このページはデータベースは不要ですから汎用的なFormViewクラスを継承します。

my_blog/views.py

```
from django.shortcuts import render
from django.views import generic
from .forms import InquiryForm


class IndexView(generic.TemplateView):
    template_name = "index.html"


class InquiryView(generic.FormView):
    template_name = "inquiry.html"
    form_class = InquiryForm
```

### フォームのフィールドを定義



my_blog/forms.py

```
from django import forms


class InquiryForm(forms.Form):
    name = forms.CharField(label='お名前', max_length=30)
    email = forms.EmailField(label='メールアドレス')
    title = forms.CharField(label='タイトル', max_length=30)
    message = forms.CharField(label='メッセージ', widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].widget.attrs['class'] = 'form-control col-9'
        self.fields['name'].widget.attrs['placeholder'] = 'お名前をここに入力してください。'

        self.fields['email'].widget.attrs['class'] = 'form-control col-11'
        self.fields['email'].widget.attrs['placeholder'] = 'メールアドレスをここに入力してください。'

        self.fields['title'].widget.attrs['class'] = 'form-control col-11'
        self.fields['title'].widget.attrs['placeholder'] = 'タイトルをここに入力してください。'

        self.fields['message'].widget.attrs['class'] = 'form-control col-12'
        self.fields['message'].widget.attrs['placeholder'] = 'メッセージをここに入力してください。'

```

### テンプレート編集

templates/base.html

```
{% load static %}

<html lang="ja">

<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
  <meta name="description" content="">
  <meta name="author" content="">

  <title>{% block title %}{% endblock %}</title>

  <!-- Bootstrap core CSS -->
  <link href="{% static 'vendor/bootstrap/css/bootstrap.min.css' %}" rel="stylesheet">

  <!-- Custom fonts for this template -->
  <link href="https://fonts.googleapis.com/css?family=Catamaran:100,200,300,400,500,600,700,800,900" rel="stylesheet">
  <link href="https://fonts.googleapis.com/css?family=Lato:100,100i,300,300i,400,400i,700,700i,900,900i"
    rel="stylesheet">

  <!-- Custom styles for this template -->
  <link href="{% static 'css/one-page-wonder.min.css' %}" rel="stylesheet">

  <!-- My style -->
  <link rel="stylesheet" type="text/css" href="{% static 'css/mystyle.css' %}">
  {% block head %}{% endblock %}
</head>

<body>
  <div id="wrapper">
    <!-- Navigation -->
    <nav class="navbar navbar-expand-lg navbar-dark navbar-custom fixed-top">
      <div class="container">
        <a class="navbar-brand" href="{% url 'my_blog:index' %}">PRIVATE DIARY</a>
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarResponsive"
          aria-controls="navbarResponsive" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarResponsive">
          <ul class="navbar-nav mr-auto">
            <li class="nav-item {% block active_inquiry %}{% endblock %}">
              <a class="nav-link" href="{% url 'my_blog:inquiry' %}">INQUIRY</a>
            </li>
          </ul>
          <ul class="navbar-nav ml-auto">
            <li class="nav-item">
              <a class="nav-link" href="#">Sign Up</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="#">Log In</a>
            </li>
          </ul>
        </div>
      </div>
    </nav>

    {% block header%}{% endblock %}

    {% block contents%}{% endblock %}

    <!-- Footer -->
    <footer class="py-5 bg-black">
      <div class="container">
        <p class="m-0 text-center text-white small">Copyright &copy; Private Dairy 2019</p>
      </div>
      <!-- /.container -->
    </footer>

    <!-- Bootstrap core JavaScript -->
    <script src="{% static 'vendor/jquery/jquery.min.js' %}"></script>
    <script src="{% static 'vendor/bootstrap/js/bootstrap.bundle.min.js' %}"></script>
  </div>
</body>

</html>
```



templates/inquiry.html

```
{% extends 'base.html' %}

{% block title %}お問い合わせ | Private Diary{% endblock %}

{% block active_inquiry %}active{% endblock %}

{% block contents %}
<div class="container">
    <div class="row">
        <div class="my-div-style">
            <form method="post">
                {% csrf_token %}

                {{ form.non_field_errors }}

                {% for field in form %}
                    <div class="form-group row">
                        <label for="{{ field.id_for_label }}" class="col-sm-4 col-form-label">
                            <strong>{{ field.label_tag }}</strong>
                        </label>
                        <div class="col-sm-8">
                            {{ field }}
                            {{ field.errors }}
                        </div>
                    </div>
                {% endfor %}

                <div class="offset-sm-4 col-sm-8">
                    <button class="btn btn-primary" type="submit">送信</button>
                </div>
            </form>
        </div>
    </div>
</div>
{% endblock %}

```

### settings.pyの編集

settings.pyを本番用とローカル用にわけます。

共通用がsettings_common.pyでローカル用がsettings_dev.pyとします。

ローカル用を動作させるには環境変数を使います。

settings_common.py

```
import os

from django.contrib.messages import constants as messages

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['SECRET_KEY']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'my_blog.apps.MyBlogConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'blog.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'blog.wsgi.application'


# データベース設定
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'my_blog',
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': '',
        'PORT': '',
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'ja'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

MESSAGE_TAGS = {
    messages.ERROR: 'alert alert-danger',
    messages.WARNING: 'alert alert-warning',
    messages.SUCCESS: 'alert alert-success',
    messages.INFO: 'alert alert-info',
}

```



settings_dev.py

```
from .settings_common import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# ロギング設定
LOGGING = {
    'version': 1,  # 1固定
    'disable_existing_loggers': False,

    # ロガーの設定
    'loggers': {
        # Djangoが利用するロガー
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
        },
        # my_blogアプリケーションが利用するロガー
        'my_blog': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    },

    # ハンドラの設定
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'dev'
        },
    },

    # フォーマッタの設定
    'formatters': {
        'dev': {
            'format': '\t'.join([
                '%(asctime)s',
                '[%(levelname)s]',
                '%(pathname)s(Line:%(lineno)d)',
                '%(message)s'
            ])
        },
    }
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

```



### ローカル環境切り替えの環境変数設定

環境変数に以下の内容を追記します。

```
export DJANGO_SETTINGS_MODULE=blog.settings_dev
```





## 認証アプリの作成

認証用のアプリは別アプリとして作成します。

そうすると他のアプリケーションにも組み込めるようになります。

最初にアプリを作成した時のようにmanage.pyを使って作成します。

accountsアプリ作成

```
python manage.py startapp accounts
```

新しいアプリを作成したので、settings.py に` 'accounts.apps.AccountsConfig' `を追加します。

settings_common.py

```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'my_blog.apps.MyBlogConfig',
    'accounts.apps.AccountsConfig',
]
```

### カスタムユーザーモデルを定義

認証アプリを作成するときは、Djangoが用意しているユーザーモデルを使うのではなく、カスタムユーザーモデルを使う方が良い。

accountsアプリがカスタムユーザーモデルを参照するようにするには次の設定を行います。

accounts/models.py

```
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    """拡張ユーザーモデル"""

    class Meta:
        verbose_name_plural = 'CustomUser'
```

settings_common.pyの最後に以下内容を追加します。

accountsフォルダ内のmodels.pyで定義したCustomUserクラスがAUTH_USER_MODELということです。

settings_common.py

```
AUTH_USER_MODEL = 'accounts.CustomUser'
```

### カスタムユーザーモデルを管理サイトに登録

管理サイトでカスタムユーザーモデルを編集できるようにするものです。

```
from django.contrib import admin
from .models import CustomUser


admin.site.register(CustomUser)
```

## マイグレーションの実行

新しくmodelを作成したり、変更した場合にモデルをデータベースに反映する作業です。

マイグレーション作業は、makemigrations と migrate の２段回のコマンドで実行します。

makemigrations

```
python manage.py makemigrations
```

結果

**Migrations for 'accounts':**

 **accounts/migrations/0001_initial.py**

  \- Create model CustomUser



migrate

```
python manage.py migrate
```

結果

**Operations to perform:**

 **Apply all migrations:** accounts, admin, auth, contenttypes, sessions

**Running migrations:**

 Applying contenttypes.0001_initial... **OK**

 Applying contenttypes.0002_remove_content_type_name... **OK**

 Applying auth.0001_initial... **OK**

 Applying auth.0002_alter_permission_name_max_length... **OK**

 Applying auth.0003_alter_user_email_max_length... **OK**

 Applying auth.0004_alter_user_username_opts... **OK**

 Applying auth.0005_alter_user_last_login_null... **OK**

 Applying auth.0006_require_contenttypes_0002... **OK**

 Applying auth.0007_alter_validators_add_error_messages... **OK**

 Applying auth.0008_alter_user_username_max_length... **OK**

 Applying auth.0009_alter_user_last_name_max_length... **OK**

 Applying auth.0010_alter_group_name_max_length... **OK**

 Applying auth.0011_update_proxy_permissions... **OK**

 Applying auth.0012_alter_user_first_name_max_length... **OK**

 Applying accounts.0001_initial... **OK**

 Applying admin.0001_initial... **OK**

 Applying admin.0002_logentry_remove_auto_add... **OK**

 Applying admin.0003_logentry_add_action_flag_choices... **OK**

 Applying sessions.0001_initial... **OK**



### 認証アプリのためのdjango-allauthのインストール

django-allauthは単純な認証の仕組み以外にOAuth認証、ソーシャル認証までサポートした機能を持っています。

今回は、サインアップ（ユーザー登録）、パスワードリセット、ログイン・ログアウト、メールアドレス認証を実施します。

#### インストール

カレントディレクトリを仮想環境のルートに戻ります。今回の作業ではdj_blogで、Djangoをインストールした場所です。

認証機能を提供するパッケージをインストールしておきます。

```
pip install django-allauth
```

### settings_commonの編集

django-allauthを活用するにはsettings_commonで編集します。

`settings_common.py` の `INSTALLED_APPS` に以下の内容を追加します。

```
'django.contrib.sites',
'allauth',
'allauth.account',
```

また、次の内容を最後の行に追加します。

```
# django-allauthで利用するdjango.contrib.sitesを使うためにサイト識別用IDを設定
SITE_ID = 1

AUTHENTICATION_BACKENDS = (
    'allauth.account.auth_backends.AuthenticationBackend',  # 一般ユーザー用(メールアドレス認証)
    'django.contrib.auth.backends.ModelBackend',  # 管理サイト用(ユーザー名認証)
)

# メールアドレス認証に変更する設定
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_USERNAME_REQUIRED = False

# サインアップにメールアドレス確認を挟むよう設定
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_EMAIL_REQUIRED = True

# ログイン/ログアウト後の遷移先を設定
LOGIN_REDIRECT_URL = 'my_blog:index'
ACCOUNT_LOGOUT_REDIRECT_URL = 'account_login'

# ログアウトリンクのクリック一発でログアウトする設定
ACCOUNT_LOGOUT_ON_GET = True

# django-allauthが送信するメールの件名に自動付与される接頭辞をブランクにする設定
ACCOUNT_EMAIL_SUBJECT_PREFIX = ''

# デフォルトのメール送信元を設定
DEFAULT_FROM_EMAIL = 'admin@example.com'

```

この時点でsettings_commonは次のようになっています。



settings_common.py

```
import os

from django.contrib.messages import constants as messages

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['SECRET_KEY']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'my_blog.apps.MyBlogConfig',
    'accounts.apps.AccountsConfig',
    'django.contrib.sites',
    'allauth',
    'allauth.account',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'blog.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'blog.wsgi.application'


# データベース設定
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'my_blog',
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': '',
        'PORT': '',
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'ja'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

MESSAGE_TAGS = {
    messages.ERROR: 'alert alert-danger',
    messages.WARNING: 'alert alert-warning',
    messages.SUCCESS: 'alert alert-success',
    messages.INFO: 'alert alert-info',
}

AUTH_USER_MODEL = 'accounts.CustomUser'

# django-allauthで利用するdjango.contrib.sitesを使うためにサイト識別用IDを設定
SITE_ID = 1

AUTHENTICATION_BACKENDS = (
    # 一般ユーザー用(メールアドレス認証)
    'allauth.account.auth_backends.AuthenticationBackend',
    'django.contrib.auth.backends.ModelBackend',  # 管理サイト用(ユーザー名認証)
)

# メールアドレス認証に変更する設定
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_USERNAME_REQUIRED = False

# サインアップにメールアドレス確認を挟むよう設定
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_EMAIL_REQUIRED = True

# ログイン/ログアウト後の遷移先を設定
LOGIN_REDIRECT_URL = 'my_blog:index'
ACCOUNT_LOGOUT_REDIRECT_URL = 'account_login'

# ログアウトリンクのクリック一発でログアウトする設定
ACCOUNT_LOGOUT_ON_GET = True

# django-allauthが送信するメールの件名に自動付与される接頭辞をブランクにする設定
ACCOUNT_EMAIL_SUBJECT_PREFIX = ''

# デフォルトのメール送信元を設定
DEFAULT_FROM_EMAIL = 'admin@example.com'

```

### ルーティングの追加

blog/urls.py

```
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('my_blog.urls')),
    path('accounts/', include('allauth.urls')),
]
```

### django-allauthのテンプレート作成

accountフォルダ内にtemplatesフォルダを作成して各ファイルを作成します。



base.html

```
{% load static %}

<html lang="ja">

<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
  <meta name="description" content="">
  <meta name="author" content="">

  <title>{% block title %}{% endblock %}</title>

  <!-- Bootstrap core CSS -->
  <link href="{% static 'vendor/bootstrap/css/bootstrap.min.css' %}" rel="stylesheet">

  <!-- Custom fonts for this template -->
  <link href="https://fonts.googleapis.com/css?family=Catamaran:100,200,300,400,500,600,700,800,900" rel="stylesheet">
  <link href="https://fonts.googleapis.com/css?family=Lato:100,100i,300,300i,400,400i,700,700i,900,900i"
    rel="stylesheet">

  <!-- Custom styles for this template -->
  <link href="{% static 'css/one-page-wonder.min.css' %}" rel="stylesheet">

  <!-- My style -->
  <link rel="stylesheet" type="text/css" href="{% static 'css/mystyle.css' %}">
  {% block head %}{% endblock %}
</head>

<body>
  <div id="wrapper">
    <!-- Navigation -->
    <nav class="navbar navbar-expand-lg navbar-dark navbar-custom fixed-top">
      <div class="container">
        <a class="navbar-brand" href="{% url 'my_blog:index' %}">My Blog</a>
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarResponsive"
          aria-controls="navbarResponsive" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarResponsive">
          <ul class="navbar-nav mr-auto">
            <li class="nav-item {% block active_inquiry %}{% endblock %}">
              <a class="nav-link" href="{% url 'my_blog:inquiry' %}">INQUIRY</a>
            </li>
          </ul>
          <ul class="navbar-nav ml-auto">
            {% if user.is_authenticated %}
            <li class="nav-item">
              <a class="nav-link" href="{% url 'account_logout' %}">Log Out</a>
            </li>
            {% else %}
            <li class="nav-item {% block active_signup %}{% endblock %}">
              <a class="nav-link" href="{% url 'account_signup' %}">Sign Up</a>
            </li>
            <li class="nav-item {% block active_login %}{% endblock %}">
              <a class="nav-link" href="{% url 'account_login' %}">Log In</a>
            </li>
            {% endif %}
          </ul>

        </div>
      </div>
    </nav>

    {% block header%}{% endblock %}
    {% if messages %}
    <div class="container">
      <div class="row">
        <div class="my-div-style w-100">
          <ul class="messages" style="list-style: none;">
            {% for message in messages %}
            <li {% if message.tags %} class="{{ message.tags }}" {% endif %}>
              {{ message }}
            </li>
            {% endfor %}
          </ul>
        </div>
      </div>
    </div>
    {% endif %}
    {% block contents%}{% endblock %}

    <!-- Footer -->
    <footer class="py-5 bg-black">
      <div class="container">
        <p class="m-0 text-center text-white small">Copyright &copy; Private Dairy 2019</p>
      </div>
      <!-- /.container -->
    </footer>

    <!-- Bootstrap core JavaScript -->
    <script src="{% static 'vendor/jquery/jquery.min.js' %}"></script>
    <script src="{% static 'vendor/bootstrap/js/bootstrap.bundle.min.js' %}"></script>
  </div>
</body>

</html>
```

### django-allauth用マイグレーション



migrate

```
python manage.py migrate
```

結果

**Operations to perform:**

 **Apply all migrations:** account, accounts, admin, auth, contenttypes, sessions, sites

**Running migrations:**

 Applying account.0001_initial... **OK**

 Applying account.0002_email_max_length... **OK**

 Applying sites.0001_initial... **OK**

 Applying sites.0002_alter_domain_unique... **OK**



この段階でローカルサーバーを動かしてログインできるかを確認します。

```
python manage.py runserver
```

## メディアファイルを使えるようにする

画像を扱うのでpillowをインストールします。

仮想環境のルートでインストールします。

```
pip install pillow
```

### MEDIA_ROOTの設定

settings_devとsettings_commonにMEDIA_ROOTの設定をします。

settings_dev.py

```
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
```

settings_common.py

```
MEDIA_URL = '/media/'
```

### プロジェクト用urls.pyの編集

開発サーバーでメディアファイルを配信するにはメディアファイル配信用ルーティングが必要です。

blog/urls.py

```
from django.contrib import admin
from django.contrib.staticfiles.urls import static
from django.urls import path, include
from . import settings_common, settings_dev

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('my_blog.urls')),
    path('accounts/', include('allauth.urls')),
]

# 開発サーバーでメディアを配信できるようにする設定
urlpatterns += static(settings_common.MEDIA_URL,
                      document_root=settings_dev.MEDIA_ROOT)

```

## Blogモデルを定義

ユーザーが作成するブログを保存するデータベースのテーブルを作成します。

データベースのテーブルはアプリ内のmodels.pyで行います。



my_blog/models.py

```
from accounts.models import CustomUser
from django.db import models


class Blog(models.Model):
    """Blogモデル"""

    user = models.ForeignKey(
        CustomUser, verbose_name='ユーザー', on_delete=models.PROTECT)
    title = models.CharField(verbose_name='タイトル', max_length=40)
    content = models.TextField(verbose_name='本文', blank=True, null=True)
    photo1 = models.ImageField(verbose_name='写真1', blank=True, null=True)
    photo2 = models.ImageField(verbose_name='写真2', blank=True, null=True)
    photo3 = models.ImageField(verbose_name='写真3', blank=True, null=True)
    created_at = models.DateTimeField(verbose_name='作成日時', auto_now_add=True)
    updated_at = models.DateTimeField(verbose_name='更新日時', auto_now=True)

    class Meta:
        verbose_name_plural = 'Blog'

    def __str__(self):
        return self.title
```

### 管理サイトの作成

アプリの中のadmin.pyを編集すると管理サイトができます。



my_blog/admin.py

```
from django.contrib import admin

from .models import Blog


admin.site.register(Blog)
```

## 日記一覧リスト作成

日記一覧リストのページを作成します。

* ルーティング
* ビュー作成
* テンプレート作成

### ルーティング



my_blog/urls.py

```
from django.urls import path

from . import views


app_name = 'my_blog'
urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),
    path('inquiry', views.InquiryView.as_view(), name='inquiry'),
    path('blog-list/', views.BlogListView.as_view(), name="blog_list"),
]
```

### viewsの作成



my_blog/views.py

```
import logging

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views import generic

from .forms import InquiryForm, BlogCreateForm
from .models import Blog

logger = logging.getLogger(__name__)


class IndexView(generic.TemplateView):
    template_name = "index.html"


class InquiryView(generic.FormView):
    template_name = "inquiry.html"
    form_class = InquiryForm
    success_url = reverse_lazy('my_blog:inquiry')

    def form_valid(self, form):
        form.send_email()
        messages.success(self.request, 'メッセージを送信しました。')
        logger.info('Inquiry sent by {}'.format(form.cleaned_data['name']))
        return super().form_valid(form)


class BlogListView(LoginRequiredMixin, generic.ListView):
    model = Blog
    template_name = 'blog_list.html'
    paginate_by = 2

    def get_queryset(self):
        blogs = Blog.objects.filter(
            user=self.request.user).order_by('-created_at')
        return blogs

```



### CSS追加

[Start Bootstrap](https://startbootstrap.com/)の[CleanBlog](https://startbootstrap.com/themes/clean-blog/)のテンプレート活用

ここは良さげなテンプレートが色々ありますね。エンジニアは潔くデザインはBootstrapに任せるのが吉。

clean-blog.min.cssを static/css に追加。

my_blogフォルダに blog_list.html を作成します。CleanBlogから持ってきたテンプレートを活用してコーディングします。

my_blog/templates/blog_list.html

```
{% extends 'base.html' %}
{% load static %}

{% block title %}日記一覧 | My Blog{% endblock %}

{% block active_my_blog_list %}active{% endblock %}

{% block head %}
<link href="{% static 'css/clean-blog.min.css' %}" rel="stylesheet">
{% endblock %}

{% block contents %}
<div class="container">
    <div class="row">
        <div class="my-div-style w-100">
            <div class="col-lg-8 col-md-10 mx-auto">
                <div class="clearfix">
                    <a class="btn btn-primary float-right" href="">新規作成</a>
                </div>
                {% for blog in blog_list %}
                <div class="post-preview">
                    <a href="">
                        <h2 class="post-title">
                            {{ blog.title }}
                        </h2>
                        <h3 class="post-subtitle">
                            {{ blog.content|truncatechars:20 }}
                        </h3>
                    </a>
                    <p class="post-meta">{{ blog.created_at }}</p>
                </div>
                <hr>
                {% empty %}
                <p>日記がありません。</p>
                {% endfor %}


            </div>
        </div>
    </div>
</div>
{% endblock %}
```

### ページネーションの追加

ページネーションをつける場合は以下を追加

```
                <!-- ページネーション処理 -->
                {% if is_paginated %}
                <ul class="pagination">
                    <!-- 前ページへのリンク -->
                    {% if page_obj.has_previous %}
                    <li class="page-item">
                        <a class="page-link" href="?page={{ page_obj.previous_page_number }}">
                            <span aria-hidden="true">&laquo;</span>
                        </a>
                    </li>
                    {% endif %}

                    <!-- ページ数表示 -->
                    {% for page_num in page_obj.paginator.page_range %}
                    {% if page_obj.number == page_num %}
                    <li class="page-item active"><a class="page-link" href="#">{{ page_num }}</a></li>
                    {% else %}
                    <li class="page-item"><a class="page-link" href="?page={{ page_num }}">{{ page_num }}</a></li>
                    {% endif %}
                    {% endfor %}

                    <!-- 次ページへのリンク -->
                    {% if page_obj.has_next %}
                    <li class="page-item">
                        <a class="page-link" href="?page={{ page_obj.next_page_number }}">
                            <span aria-hidden="true">&raquo;</span>
                        </a>
                    </li>
                    {% endif %}
                </ul>
                {% endif %}
```



ページネーションを加えたblog_list.html

```
{% extends 'base.html' %}
{% load static %}

{% block title %}日記一覧 | My Blog{% endblock %}

{% block active_my_blog_list %}active{% endblock %}

{% block head %}
<link href="{% static 'css/clean-blog.min.css' %}" rel="stylesheet">
{% endblock %}

{% block contents %}
<div class="container">
    <div class="row">
        <div class="my-div-style w-100">
            <div class="col-lg-8 col-md-10 mx-auto">
                <div class="clearfix">
                    <a class="btn btn-primary float-right" href="">新規作成</a>
                </div>
                {% for blog in blog_list %}
                <div class="post-preview">
                    <a href="">
                        <h2 class="post-title">
                            {{ blog.title }}
                        </h2>
                        <h3 class="post-subtitle">
                            {{ blog.content|truncatechars:20 }}
                        </h3>
                    </a>
                    <p class="post-meta">{{ blog.created_at }}</p>
                </div>
                <hr>
                {% empty %}
                <p>日記がありません。</p>
                {% endfor %}

                <!-- ページネーション処理 -->
                {% if is_paginated %}
                <ul class="pagination">
                    <!-- 前ページへのリンク -->
                    {% if page_obj.has_previous %}
                    <li class="page-item">
                        <a class="page-link" href="?page={{ page_obj.previous_page_number }}">
                            <span aria-hidden="true">&laquo;</span>
                        </a>
                    </li>
                    {% endif %}

                    <!-- ページ数表示 -->
                    {% for page_num in page_obj.paginator.page_range %}
                    {% if page_obj.number == page_num %}
                    <li class="page-item active"><a class="page-link" href="#">{{ page_num }}</a></li>
                    {% else %}
                    <li class="page-item"><a class="page-link" href="?page={{ page_num }}">{{ page_num }}</a></li>
                    {% endif %}
                    {% endfor %}

                    <!-- 次ページへのリンク -->
                    {% if page_obj.has_next %}
                    <li class="page-item">
                        <a class="page-link" href="?page={{ page_obj.next_page_number }}">
                            <span aria-hidden="true">&raquo;</span>
                        </a>
                    </li>
                    {% endif %}
                </ul>
                {% endif %}
            </div>
        </div>
    </div>
</div>
{% endblock %}
```



また、ページネーションを追加する場合はviews.pyでBlogListViewに `aginate_by = 2` を追加します。

my_blog/views.py

```
class BlogListView(LoginRequiredMixin, generic.ListView):
    model = Blog
    template_name = 'blog_list.html'
    paginate_by = 2

    def get_queryset(self):
        blogs = Blog.objects.filter(
            user=self.request.user).order_by('-created_at')
        return blogs
```



#### 遷移の仕組み

my_blog/settings_common.py

```
LOGIN_REDIRECT_URL = 'blog:blog_list'
```

### base.htmlの編集

```
<li class="nav-item {% block active_inquiry %}{% endblock %}">
   <a class="nav-link" href="{% url 'my_blog:inquiry' %}">INQUIRY</a>
</li>
```

以上の内容の次に以下内容を追加

```
{% if user.is_authenticated %}
   <li class="nav-item {% block active_diary_list %}{% endblock %}">
     <a class="nav-link" href="{% url 'diary:diary_list' %}">DIARY LIST</a>
   </li>
{% endif %}

```



my_blog/templates/base.html

```
{% load static %}

<html lang="ja">

<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
  <meta name="description" content="">
  <meta name="author" content="">

  <title>{% block title %}{% endblock %}</title>

  <!-- Bootstrap core CSS -->
  <link href="{% static 'vendor/bootstrap/css/bootstrap.min.css' %}" rel="stylesheet">

  <!-- Custom fonts for this template -->
  <link href="https://fonts.googleapis.com/css?family=Catamaran:100,200,300,400,500,600,700,800,900" rel="stylesheet">
  <link href="https://fonts.googleapis.com/css?family=Lato:100,100i,300,300i,400,400i,700,700i,900,900i"
    rel="stylesheet">

  <!-- Custom styles for this template -->
  <link href="{% static 'css/one-page-wonder.min.css' %}" rel="stylesheet">

  <!-- My style -->
  <link rel="stylesheet" type="text/css" href="{% static 'css/mystyle.css' %}">
  {% block head %}{% endblock %}
</head>

<body>
  <div id="wrapper">
    <!-- Navigation -->
    <nav class="navbar navbar-expand-lg navbar-dark navbar-custom fixed-top">
      <div class="container">
        <a class="navbar-brand" href="{% url 'my_blog:index' %}">My Blog</a>
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarResponsive"
          aria-controls="navbarResponsive" aria-expanded="false" aria-label="Toggle navigation">
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarResponsive">
          <ul class="navbar-nav mr-auto">
            <li class="nav-item {% block active_inquiry %}{% endblock %}">
              <a class="nav-link" href="{% url 'my_blog:inquiry' %}">INQUIRY</a>
            </li>
            {% if user.is_authenticated %}
            <li class="nav-item {% block active_diary_list %}{% endblock %}">
              <a class="nav-link" href="{% url 'diary:diary_list' %}">DIARY LIST</a>
            </li>
            {% endif %}

          </ul>
          <ul class="navbar-nav ml-auto">
            {% if user.is_authenticated %}
            <li class="nav-item">
              <a class="nav-link" href="{% url 'account_logout' %}">Log Out</a>
            </li>
            {% else %}
            <li class="nav-item {% block active_signup %}{% endblock %}">
              <a class="nav-link" href="{% url 'account_signup' %}">Sign Up</a>
            </li>
            <li class="nav-item {% block active_login %}{% endblock %}">
              <a class="nav-link" href="{% url 'account_login' %}">Log In</a>
            </li>
            {% endif %}
          </ul>

        </div>
      </div>
    </nav>

    {% block header%}{% endblock %}
    {% if messages %}
    <div class="container">
      <div class="row">
        <div class="my-div-style w-100">
          <ul class="messages" style="list-style: none;">
            {% for message in messages %}
            <li {% if message.tags %} class="{{ message.tags }}" {% endif %}>
              {{ message }}
            </li>
            {% endfor %}
          </ul>
        </div>
      </div>
    </div>
    {% endif %}
    {% block contents%}{% endblock %}

    <!-- Footer -->
    <footer class="py-5 bg-black">
      <div class="container">
        <p class="m-0 text-center text-white small">Copyright &copy; Private Dairy 2019</p>
      </div>
      <!-- /.container -->
    </footer>

    <!-- Bootstrap core JavaScript -->
    <script src="{% static 'vendor/jquery/jquery.min.js' %}"></script>
    <script src="{% static 'vendor/bootstrap/js/bootstrap.bundle.min.js' %}"></script>
  </div>
</body>

</html>
```



forms.py

```
from django import forms
from django.core.mail import EmailMessage
from .models import Blog


class InquiryForm(forms.Form):
    name = forms.CharField(label='お名前', max_length=30)
    email = forms.EmailField(label='メールアドレス')
    title = forms.CharField(label='タイトル', max_length=30)
    message = forms.CharField(label='メッセージ', widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['name'].widget.attrs['class'] = 'form-control col-9'
        self.fields['name'].widget.attrs['placeholder'] = 'お名前をここに入力してください。'

        self.fields['email'].widget.attrs['class'] = 'form-control col-11'
        self.fields['email'].widget.attrs['placeholder'] = 'メールアドレスをここに入力してください。'

        self.fields['title'].widget.attrs['class'] = 'form-control col-11'
        self.fields['title'].widget.attrs['placeholder'] = 'タイトルをここに入力してください。'

        self.fields['message'].widget.attrs['class'] = 'form-control col-12'
        self.fields['message'].widget.attrs['placeholder'] = 'メッセージをここに入力してください。'

    def send_email(self):
        name = self.cleaned_data['name']
        email = self.cleaned_data['email']
        title = self.cleaned_data['title']
        message = self.cleaned_data['message']

        subject = 'お問い合わせ {}'.format(title)
        message = '送信者名: {0}\nメールアドレス: {1}\nメッセージ:\n{2}'.format(
            name, email, message)
        from_email = 'admin@example.com'
        to_list = [
            'test@example.com'
        ]
        cc_list = [
            email
        ]

        message = EmailMessage(subject=subject, body=message,
                               from_email=from_email, to=to_list, cc=cc_list)
        message.send()


class BlogCreateForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ('title', 'content', 'photo1', 'photo2', 'photo3', )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

```







この時点でBlogモデルをデータベースに反映するために、マイグレーションを行います。

makemigrations

```
python manage.py makemigrations
```

結果

**Migrations for 'my_blog':**

 **my_blog/migrations/0001_initial.py**

  \- Create model Blog



migrate

```
python manage.py migrate
```

結果

**Operations to perform:**

 **Apply all migrations:** account, accounts, admin, auth, contenttypes, my_blog, sessions, sites

**Running migrations:**

 Applying my_blog.0001_initial... **OK**



## スーパーユーザーの作成

スーパーユーザーを作成する場合、ユーザー名とメールアドレスとパスワードを聞いてきますので、それぞれ入力します。

```
python manage.py createsuperuser --settings blog.settings_dev
```

結果

ユーザー名: tahara

メールアドレス: aaaa@example.com

Password: 

Password (again): 

Superuser created successfully.





1. 再びrunseverを起動します。

```
python manage.py runserver
```

2. 次のアドレスでadmin画面に入れます。
   http://127.0.0.1:8000/admin/
3. Django管理サイトの認証画面になりますので、先に作ったスーパーユーザーで認証します。
4. My_Blogの追加ボタンをクリック
5. ブログ入力エディタが出てくるので記事を書く
6. http://127.0.0.1:8000/blog-list/で先程の記事が一覧の中に表示される（最初は当然１つの記事のタイトルだけ



