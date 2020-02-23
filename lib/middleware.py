from django.utils.deprecation import MiddlewareMixin

from common import errors
from lib.http import render_json
from user.models import User


class Authmiddleware(MiddlewareMixin):
    def process_request(self, request):
        uid = request.session.get('uid')
        WHITE_LIST = ['/api/user/submit/phone/', '/api/user/submit/vcode/']
        if request.path in WHITE_LIST:
            return
        if uid:
            try:
                user = User.objects.get(id=uid)
                request.user = user
                return
            except User.DoesNotExist:
                return render_json(code=errors.USER_ERROR, data='用户不存在')
        else:
            return render_json(code=errors.LOGIN_ERROR, data='请先登录')

