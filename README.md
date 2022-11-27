# くだらんきんぐ - kudaranking

## [URL](http://52.192.6.119/)

公開を終えて、AWSにデプロイし直したものです。

(一応デプロイしている程度なので、httpです。また、DBも初期化してしまったので、利用者はいません。ご了承ください。)

下記のTwitterは公開当時動かしていたものです。

[twitter](https://twitter.com/kudaranking) 

## サイト概要
ランキングを作成や参加して、コメントを楽しむものです。

競い合いから話のネタ作りまで自由に利用してください。

## 機能一覧
- ユーザー名とパスワードによる登録・ログイン
- Twitterログイン
- マイページ
- ランキングページの作成
- ランキングの参加と投稿
- ランキングページ(sort, 偏差値算出)
- コメント欄(非同期通信)

## 実行手順
python3のcommandの2パターン

> ① 初compose up

`command: bash -c "python manage.py migrate && export DJANGO_SUPERUSER_USERNAME=${ROOT_NAME} && export DJANGO_SUPERUSER_EMAIL=${ROOT_MAIL} && export DJANGO_SUPERUSER_PASSWORD=${ROOT_PASSWORD} && python manage.py createsuperuser --no-input && python manage.py collectstatic && supervisord && uwsgi --socket :8001 --module webranking.wsgi --py-autoreload 1"`

> ② 2回目以降のcompose up

`command: bash -c "supervisord && uwsgi --socket :8001 --module webranking.wsgi --py-autoreload 1"`

> docker-compose up

`docker-compose up --build --remove-orphans -d`


## メモ
[参考]channels を用いたdjangoをdockerで共存させる方法

https://libproc.com/django-channels-with-wsgi-asgi-in-docker-nginx-supervisor/

https://github.com/daikidomon/nginx-django-channels/tree/supervisord
