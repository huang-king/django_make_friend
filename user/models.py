from datetime import datetime

from django.db import models



# Create your models here.
from lib.orm import ModelMixin

SEX = (
    ('female', 'female'),
    ('male', 'male'),
)


class User(models.Model):
    """
    用户信息
    """
    phonenum = models.CharField(max_length=20, unique=True, verbose_name='手机号')
    nickname = models.CharField(max_length=128, unique=True, verbose_name='昵称')
    sex = models.CharField(max_length=20, choices=SEX, verbose_name='性别')
    birth_year = models.IntegerField(default=2000, verbose_name='出生年')
    birth_month = models.IntegerField(default=1, verbose_name='出生月')
    birth_day = models.IntegerField(default=1, verbose_name='出生日')
    avatar = models.CharField(max_length=255, verbose_name='个人形象')
    location = models.CharField(max_length=64, verbose_name='常居地')

    def __str__(self):
        return f'<User {self.nickname}>'

    class Meta:
        db_table = 'user'

    @property
    def year_detail(self):
        today = datetime.now()
        birthday = datetime(year=self.birth_year,
                            month=self.birth_month,
                            day=self.birth_day)
        detail = int((birthday - today).days // 365)
        return detail

    def to_dict(self):
        return {
            'phonenum': self.phonenum,
            'nickname': self.nickname,
            'sex': self.sex,
            'age': self.year_detail,
            'avatar': self.avatar,
            'location': self.location
        }

    @property
    def profile(self):
        # 获取用户的profile
        if not hasattr(self, 'profile_'):
            self.profile_, _ = Profile.objects.get_or_create(id=self.id)
        return self.profile_


class Profile(models.Model, ModelMixin):
    location = models.CharField(max_length=64, verbose_name='目标城市')
    min_distance = models.IntegerField(default=1, verbose_name='最小查找范围')
    max_distance = models.IntegerField(default=50, verbose_name='最大查找范围')
    min_dating_age = models.IntegerField(default=18, verbose_name='最小交友年龄')
    max_dating_age = models.IntegerField(default=50, verbose_name='最大交友年龄')
    dating_sex = models.CharField(max_length=32, choices=SEX, verbose_name='匹配的性别')
    vibration = models.BooleanField(default=True, verbose_name='开启震动')
    only_matche = models.BooleanField(default=True, verbose_name='不让为匹配的人看我的相册')
    auto_play = models.BooleanField(default=True, verbose_name='自动播放视频')

    class Meta:
        db_table = 'Profile'
