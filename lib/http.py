""" 封装返回json操作"""
import json

from django.http import HttpResponse
from django.conf import settings
def render_json(code=0, data=None):
    if not isinstance(data, dict):
        raise TypeError('not a dict')
    dic = {
        'code': code,
        'data': data
    }
    if settings.DEBUG:
        dic = json.dumps(dic, ensure_ascii=False, indent=4, sort_keys=True)
    else:
        dic = json.dumps(dic, ensure_ascii=False, separators=[',', ':'])
    return HttpResponse(dic)

