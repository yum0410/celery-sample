import os
from celery import Celery
import cv2
import time

celery = Celery(__name__)
celery.conf.broker_url = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379')
celery.conf.result_backend = os.environ.get('CELERY_BACKEND_URL', 'redis://localhost:6379')


@celery.task(name='tasks.embed_approval_img')
def embed_approval_img(img_dir):
    """
    承認画像を埋め込む

    Parameters
    ----------
    img : fastapi File Object
        埋め込み対象の画像

    Returns
    -------
    embedded_img : Image
        埋め込み対象の画像に承認画像が埋め込まれた画像
    """
    base_img = cv2.imread(img_dir)

    stamp_img = cv2.imread('./approved.png', cv2.IMREAD_UNCHANGED)
    stamp_img = cv2.resize(stamp_img, dsize=None, fx=0.1, fy=0.1)
    height, width = stamp_img.shape[:2]

    # 貼り付け先座標の設定。とりあえず左上に
    x1, y1, x2, y2 = 0, 0, width, height
    # 合成
    base_img[y1:y2, x1:x2] = base_img[y1:y2, x1:x2] * (1 - stamp_img[:, :, 3:] / 255) + \
                        stamp_img[:, :, :3] * (stamp_img[:, :, 3:] / 255)
    # 上書き
    embedded_img_path = img_dir.replace('/org/', '/embed/', 1)
    cv2.imwrite(embedded_img_path, base_img)
    return embedded_img_path

"""
Celery_TaskのreturnにImageObjectは使用できない。
プリミティブなもののみ
"""