import os
from urllib.parse import urljoin

from django.core.cache import cache
from swiper_django import settings, other_config

from lib.sms import send_vcode
from common import errors
from lib.http import render_json
from common import keys
from user.forms import ProfileForm
from user.logic import handle_uploaded_file
from user.models import User
# Create your views here.

"""
获取短信验证
通过验证码登录、注册
获取个人资料
修改个人资料
头像上传
"""


def submit_phone(request):
    """提交手机号码"""
    phone = request.POST.get('phone')
    """发送验证码"""
    msg = send_vcode.delay(phone)
    return render_json()


def submit_vcode(request):
    """通过验证码登录、注册"""
    phone = request.POST.get('phone')
    vcode = request.POST.get('vocde')

    cache_vcode = cache.get(keys.CACHE_VCODE % phone)
    if vcode == str(cache_vcode):
        # 判断登录或者注册
        user, _ = User.objects.get_or_create(phonenum=phone, defaults={'nickname': phone})
        request.session['uid'] = user.id
        return None
    return render_json(code=errors.VCODE_ERROR, data='验证错误')


def get_proifle(request):
    """获取个人资料"""
    user = request.user
    return render_json(data=user.profile.to_dict())


def up_profile(request):
    """修改个人资料"""
    user = request.user
    form = ProfileForm(request.POST)
    if form.is_valid():
        profile = form.save(commit=False)
        profile.id = user.id
        profile.save()
        return render_json(data=profile.to_dict())
    return render_json(code=errors.PROFILE_ERROR, data='数据非法')

def upload_avatar(request):
    """头像上传"""
    user = request.user
    avatar = request.FILES.get('avatar')
    handle_uploaded_file.delay(user.uid, avatar)
    avatar_url = urljoin(other_config.QINIU_URL, keys.AVATAR_NAME % user.uid)
    user.avatar = avatar_url
    user.save()
    return render_json()








