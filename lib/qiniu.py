import os

from qiniu import Auth, put_file, etag

from common import keys
from swiper_django import other_config, settings

#需要填写你的 Access Key 和 Secret Key
access_key = other_config.QINIU_ACCESSKEY
secret_key = other_config.QINIU_SECRETKEY

#构建鉴权对象
q = Auth(access_key, secret_key)

def upload_qiniu(uid):
    # 要上传的空间
    bucket_name = 'swiper_django'

    # 上传后保存的文件名
    key = keys.AVATAR_NAME % uid

    # 生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, key, 3600)

    # 要上传文件的本地路径
    filename = keys.AVATAR_NAME % uid
    filepath = os.path.join(settings.BASE_DIR, settings.MEDIA_ROOT, filename)

    ret, info = put_file(token, key, filepath)
    # print(info.status_code)
    if info.status_code == 200:
        return True
    return False


