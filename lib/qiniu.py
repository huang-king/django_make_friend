import os

from qiniu import Auth, put_file, etag

from common import keys
from swiper_django import other_config, settings

#需要填写你的 Access Key 和 Secret Key
access_key = other_config.QINIU_ACCESSKEY
secret_key = other_config.QINIU_SECRETKEY

#构建鉴权对象
q = Auth(access_key, secret_key)

# def upload_qiniu()


