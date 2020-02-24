import os

from common import keys
from lib.qiniu import upload_qiniu
from swiper_django import settings
from worker import celery_app


@celery_app.task
def handle_uploaded_file(uid, avatar):
    filename = keys.AVATAR_NAME % uid
    filepath = os.path.join(settings.BASE_DIR, settings.MEDIA_ROOT, filename)
    if os.path.exists(filepath):
        pass
    else:
        os.mkdir(filepath)
    with open(filepath, 'wb+')as fp:
        for chunk in avatar.chunks():
            fp.write(chunk)
    if upload_qiniu(uid):
        return True
    return False
