# くだらんきんぐ - kudaranking

## [URL : https://kudaranking.net](https://kudaranking.net/)

2021年にherokuで公開していたものをAWSにデプロイし直したものです。

(DBを初期化してしまったので、利用者はいません。ご了承ください。)

下記のTwitterは公開当時動かしていたものです。

[twitter](https://twitter.com/kudaranking) 

## 概要
ランキングの作成や参加し、コメントを楽しむものです。

競い合いから話のネタ作りまで自由に利用してください。

[aboutページ](https://kudaranking.net/aboutpage/) 

## 機能一覧
- ユーザー名とパスワードによる登録・ログイン
- Twitterログイン
- マイページ
- ランキングページの作成
- ランキングの参加と投稿
- ランキングページ(sort, 偏差値算出)
- コメント欄(非同期通信)

## 利用したツール
 - server : AWS-EC2
 - DNS : AWS-Route53
 - FrameWork : Django
 - web server software : nginx
 - コンテナ : docker

## 実行手順
python3のcommandの2パターン

> ① 初compose upのdocker-compose.yml

`command: bash -c "python manage.py migrate && export DJANGO_SUPERUSER_USERNAME=${ROOT_NAME} && export DJANGO_SUPERUSER_EMAIL=${ROOT_MAIL} && export DJANGO_SUPERUSER_PASSWORD=${ROOT_PASSWORD} && python manage.py createsuperuser --no-input && python manage.py collectstatic && supervisord && uwsgi --socket :8001 --module webranking.wsgi --py-autoreload 1"`

> ② 2回目以降のcompose upのdocker-compose.yml

`command: bash -c "supervisord && uwsgi --socket :8001 --module webranking.wsgi --py-autoreload 1"`

> docker-compose up

`docker-compose up --build --remove-orphans -d`


## メモ
[参考]channels を用いたdjangoをdockerで共存させる方法

https://libproc.com/django-channels-with-wsgi-asgi-in-docker-nginx-supervisor/

https://github.com/daikidomon/nginx-django-channels/tree/supervisord

[参考]Redis Pub/Sub
https://reffect.co.jp/laravel/redis-pub-sub-dont-understand

https://tech.buysell-technologies.com/entry/adventcalendar2021-12-11
