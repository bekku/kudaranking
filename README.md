# くだらんきんぐ - kudaranking

## [URL](http://52.192.6.119/)

公開を終えて、AWSにデプロイし直したものです。(一応デプロイしている程度なので、httpです。ご了承ください。)

下記のTwitterは公開当時動かしていたものです。

[twitter](https://twitter.com/kudaranking) 

## サイト概要
ランキングを作成や参加して、コメントを楽しむものです。

競い合いから話のネタ作りまで自由に利用してください。

## 機能一覧
- ユーザー名とパスワードによる登録・ログイン
- ~~Twitterログイン~~
- マイページ
- ランキングページの作成
- ランキングの参加と投稿
- ランキングページ(sort, 偏差値算出)
- コメント欄(非同期通信)

## 実行手順
`docker-compose up --build --remove-orphans -d`
``

## メモ
[参考]channels を用いたdjangoをdockerで共存させる方法

https://libproc.com/django-channels-with-wsgi-asgi-in-docker-nginx-supervisor/

https://github.com/daikidomon/nginx-django-channels/tree/supervisord
