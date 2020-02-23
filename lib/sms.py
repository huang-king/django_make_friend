import random
import requests

from swiper_django import other_config
from django.core.cache import cache
from common import keys

def get_vcode(size=4):
    """1000-9999"""
    start = 10 ** (size -1)
    end = 10 ** size - 1
    vcode = random.randint(start, end)
    return vcode

def send_vcode(phone):
    url = other_config.YZX_URL
    params = other_config.YZX_PARAMS.copy()
    params['mobile'] = phone
    vocde = get_vcode()
    params['param'] = vocde
    cache.set(keys.VCODE_KEY % phone, vocde, timeout=180)
    resp = requests.post(url, json=params)
    if resp.status_code == 200:
        result = resp.json()
        if result['code'] == '000000':
            return 'OK'
        else:
            return result['msg']
    else:
        return '发送短信有误'
