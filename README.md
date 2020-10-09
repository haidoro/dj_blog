# DjangoでBlog作成

## 設計

### 画面イメージ

簡単な画面イメージを作成します。



#### URLと完成イメージ

| 画面名           | URL（ホスト名以降）    |
| ---------------- | ---------------------- |
| トップページ     | `/`                    |
| 問い合せページ   | `/inquiry/`            |
| ブログ一覧ページ | `/diary-list/`         |
| ブログ作成ページ | `/diary-create/`       |
| ブログ詳細ページ | `/diary-detail/<key>/` |
| ブログ編集ページ | `/diary-update/<key>/` |
| ブログ削除ページ | `/diary-delete/<key>/` |

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
            <a class="navbar-brand" href="{% url 'diary:index' %}">PRIVATE DIARY</a>
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



