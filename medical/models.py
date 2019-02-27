from django.db import models
from django.core.validators import RegexValidator

class Hospital(models.Model):
    name = models.CharField(max_length=30, unique=True, null=False, verbose_name="医院名", help_text="唯一医院名") # 唯一
    description = models.CharField(max_length=200, blank=True, verbose_name="简介", help_text="允许为空的简介")   # 允许为空
    tel = models.CharField(max_length=16, blank=True, verbose_name="联系方式", help_text="允许为空的联系方式",
                           validators=[RegexValidator(regex=r'((\d{11})|^((\d{7,8})|(\d{4}|\d{3})-(\d{7,8})|(\d{4}|\d{3})-(\d{7,8})-(\d{4}|\d{3}|\d{2}|\d{1})|(\d{7,8})-(\d{4}|\d{3}|\d{2}|\d{1}))$)')])
    # 允许为空，正则匹配11位手机号码，3-4位区号，7-8位直播号码，1－4位分机号
    email = models.EmailField(blank=True, verbose_name="电子邮箱", help_text="允许为空的电子邮箱")
    detail = models.TextField(blank=True, verbose_name="医院详情", help_text="允许为空的详情")

    class Meta:
        verbose_name = "医院"
        verbose_name_plural = "多个医院"