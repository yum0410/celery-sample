from typing import Optional, Any
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from pydantic import BaseModel
import datetime
import os
import shutil
from tasks import celery, embed_approval_img


app = FastAPI()
SAVE_DIR = './img/org/'


class TaskStatus(BaseModel):
    id: str
    status: Optional[str]
    result: Optional[Any]


@app.post('/upload', response_model=str)
def upload_image(file: UploadFile = File(...)):
    """
    埋め込み画像をアップロード

    Parameters
    ----------
    file : fastapi File Object
        埋め込み対象の画像

    Returns
    -------
    file_id : str
        画像のID(アップロード時刻+ファイル名)
    """
    now = datetime.datetime.now()
    file_name = now.strftime('%Y%m%d%H%M%S') + '_' + file.filename
    upload_dir = open(os.path.join(SAVE_DIR, file_name), 'wb+')
    shutil.copyfileobj(file.file, upload_dir)
    upload_dir.close()
    return file_name


@app.get('/embed/{file_id}', response_model=TaskStatus, response_model_exclude_unset=True)
def embedding_approval_img(file_id: str):
    """
    承認画像を埋め込む

    Parameters
    ----------
    file_id : str
        埋め込み対象の画像ID
        画像IDはupload_imageのレスポンスで取得

    Returns
    -------
    TaskStatus : TaskStatus Object
        id : タスクID
    """
    upload_img_path = os.path.join(SAVE_DIR, file_id)
    task = embed_approval_img.delay(upload_img_path)
    return TaskStatus(id=task.id)


@app.get('/check/{task_id}', response_model=TaskStatus)
def check_status(task_id: str):
    """
    Celeryタスクのステータスを確認する

    Parameters
    ----------
    task_id : str
        タスクID(embedding_approval_imgで取得)

    Returns
    -------
    TaskStatus : TaskStatus Object
        id : タスクID
        status : タスクの状態
        result : タスクの結果(完了した場合はファイル名が登録)
    """
    result = celery.AsyncResult(task_id)
    status = TaskStatus(id=task_id, status=result.status, result=result.result)
    return status


@app.get('/download/{task_id}')
async def download(task_id: str):
    """
    任意のファイルをダウンロード

    Parameters
    ----------
    task_id : str
        タスクID(embedding_approval_imgで取得)

    Returns
    -------
    response : FileResponse
        ダウンロード対象のファイルobject
    """
    result = celery.AsyncResult(task_id)
    return FileResponse(result.result)
