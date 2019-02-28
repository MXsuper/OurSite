"""
-------------------------------------------------
   Author :        lin
   date：          2019/2/27 9:41
-------------------------------------------------
"""
__author__ = 'lin'

from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User
from django.utils import timezone



# 建立城市自关联数据库表
class Areas(models.Model):
    area_id = models.AutoField(primary_key=True)
    area_name = models.CharField(max_length=20, verbose_name='名称')
    area_parent = models.ForeignKey('self', on_delete=models.SET_NULL,
                              related_name='subs', null=True,
                               blank=True, verbose_name='上级行政区划')

    class Meta:
        verbose_name = '行政区划'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.area_name

class Hospital(models.Model):
    hospital_id = models.AutoField(primary_key=True)  # 主键
    hospital_name = models.CharField(max_length=30, unique=True, null=False, verbose_name="医院名", help_text="唯一医院名") # 唯一
    hospital_desc = models.CharField(max_length=200, blank=True, verbose_name="简介", help_text="允许为空的简介")   # 允许为空
    hospital_province = models.ForeignKey('Areas', on_delete=models.PROTECT, related_name="hospital_province",
                                          help_text="省")
    hospital_city = models.ForeignKey('Areas', on_delete=models.PROTECT, related_name="hospital_city",
                                          help_text="市")
    hospital_district = models.ForeignKey('Areas', on_delete=models.PROTECT, related_name="hospital_district",
                                          help_text="区县")
    hospital_address = models.CharField(max_length=50, blank=True, verbose_name="区县以下地址", help_text="允许为空的区县以下地址")   # 允许为空
    hospital_tel = models.CharField(max_length=16, blank=True, verbose_name="联系方式", help_text="允许为空的联系方式",
                           validators=[RegexValidator(regex=r'((\d{11})|^((\d{7,8})|(\d{4}|\d{3})-(\d{7,8})|(\d{4}|\d{3})-(\d{7,8})-(\d{4}|\d{3}|\d{2}|\d{1})|(\d{7,8})-(\d{4}|\d{3}|\d{2}|\d{1}))$)')])
    # 允许为空，正则匹配11位手机号码，3-4位区号，7-8位直播号码，1－4位分机号
    hospital_email = models.EmailField(blank=True, verbose_name="电子邮箱", help_text="允许为空的电子邮箱")
    hospital_detail = models.TextField(blank=True, verbose_name="医院详情", help_text="允许为空的详情")

    class Meta:
        verbose_name = "医院"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.hospital_name

class Diagnosis(models.Model):
    diagnosis_id = models.AutoField(primary_key=True)
    diagnosis_title = models.CharField(max_length=30, verbose_name="诊断标题", help_text="诊断标题")
    diagnosis_note = models.CharField(max_length=200, default="无", verbose_name="备注信息", help_text="备注信息")
    diagnosis_image = models.ImageField(upload_to="diagnosis/images/",verbose_name="眼底图",help_text='用户上传眼底图')
    diagnosis_prop = models.CharField(max_length=10, null=False, verbose_name="诊断结果",help_text='诊断结果')
    diagnosis_addtime = models.DateTimeField(null=False,default=timezone.now,verbose_name="诊断时间",help_text='诊断时间')
    user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE, help_text='用户名')

    class Meta:
        verbose_name = "诊断结果"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.diagnosis_title

class Messages(models.Model):
    # 信息发送者
    sender = models.CharField(max_length=30, verbose_name="message_sender")
    # sender = models.ForeignKey(User, related_name='message_sender', on_delete=models.CASCADE)
    # 信息接收者
    receiver = models.CharField(max_length=30)
    # receiver = models.ForeignKey(User, related_name='message_receiver', on_delete=models.CASCADE)
    # 信息内容
    body = models.CharField(max_length=1024, verbose_name='message_body')
    # 发送时间
    created = models.DateTimeField(auto_now_add=True)
    # 状态
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.body

    class Meta:
        verbose_name = 'messages'
        verbose_name_plural = verbose_name