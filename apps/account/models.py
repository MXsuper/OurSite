from django.db import models

# Create your models here.

from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    ''' 基本用户
        django内置用户、昵称、性别、所在市、电话、生日、简介
        姓名、身份证号、医师资格证、 医生所在医院
    '''
    nickname = models.CharField(max_length=150, blank=True)
    gender = models.BooleanField(default=False, verbose_name="女生（默认男生）")
    location = models.CharField(max_length=150, blank=True)
    phone = models.CharField(max_length=20, blank=True)
    # 2012-09-04 06:00
    birthday = models.DateTimeField(auto_now_add=True)
    introduction = models.TextField(blank=True)
    is_doctor = models.BooleanField(default=False, verbose_name="医生（默认普通用户）")

    identity_name = models.CharField(max_length=150, blank=True)
    identity_number = models.CharField(max_length=150, blank=True)
    doctor_number = models.CharField(max_length=150, blank=True)
    doctor_hospital = models.CharField(max_length=150, blank=True)

    class Meta:
        verbose_name = "用户"# 设置名字
        verbose_name_plural = verbose_name # 设置复数形态时候的名字

    def __str__(self):
        return self.username

