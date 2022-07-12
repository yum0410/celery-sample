# Celeryサンプルアプリ（承認スタンプ押印アプリ）

Celeryを使った非同期タスクのサンプルアプリ

* **FastAPI** APIを提供。アップロードした画像に対して、承認スタンプを押す（画像合成タスク）
* **Celery** タスク管理
* **Flower** タスクの状態監視のダッシュボードを提供
* **Redus**  タスクのキューをメモリ上に保存

# 使い方

## 起動

```bash
# Build images
docker compose build

# Run containers
docker compose up

# Stop containers
docker compose down
```

## タスク実行

```bash
# 画像ファイルをアップロード
curl -L -F "file=@~/img.jpeg" http://http://127.0.0.1:8080/upload
# >> "20220712093434_img.jpeg"

# 画像合成タスクの実行　=> こちらが非同期部分
curl http://127.0.0.1:8080/embed/20220712093434_img.jpeg
# >> {"id":"eeea5c1b-a8d2-40dd-a095-0ed9d0731662"}

# タスクの状態確認
curl 'http://127.0.0.1:8080/check/eeea5c1b-a8d2-40dd-a095-0ed9d0731662'
# >> {"id":"eeea5c1b-a8d2-40dd-a095-0ed9d0731662","status":"SUCCESS","result":"./img/embed/20220712093434_an-pan.jpeg"}

# 合成した画像のダウンロード
curl -L 'http://127.0.0.1:8080/download/eeea5c1b-a8d2-40dd-a095-0ed9d0731662' -o embedded_img.jpeg
```

## API一覧の確認

`http://127.0.0.1:8080/docs`



## Flowerダッシュボード確認

`http://127.0.0.1:5556`


# 参考

* [CeleryによるPythonベース非同期タスク処理](https://zenn.dev/dhirooka/articles/c8fbc592f89ffc)
* [Celery](https://docs.celeryq.dev/en/stable/getting-started/introduction.html)
* [Flower](https://flower.readthedocs.io/en/latest/)
* [FastAPI](https://fastapi.tiangolo.com/ja/)