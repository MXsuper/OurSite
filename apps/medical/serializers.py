"""
-------------------------------------------------
   Author :        lin
   date：          2019/2/27 9:41
-------------------------------------------------
"""
__author__ = 'lin'
from rest_framework import serializers
from .models import *
from utils.net.classify import classify
from OurSite.settings import MEDIA_ROOT
import os

class HospitalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = '__all__'

class AreaSerializer(serializers.ModelSerializer):
    """
    行政区划信息序列化器
    """
    class Meta:
        model = Areas
        fields = ('area_id', 'area_name')

class SubAreaSerializer(serializers.ModelSerializer):
    """
    子行政区划信息序列化器
    """
    subs = AreaSerializer(many=True, read_only=True)

    class Meta:
        model = Areas
        fields = ('area_id', 'area_name', 'subs')

class DiagnosisSerializer(serializers.ModelSerializer):
    # user = UserDetailSerializer()['username'] # 嵌套外键所有字段
    user = serializers.ReadOnlyField(source="user.pk")
    # user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    class Meta:
        model = Diagnosis
        fields = '__all__'

class DiagnosisCreateSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )# 获得当前登录用户
    # user = serializers.ReadOnlyField(source="user.username")
    diagnosis_prop = serializers.SerializerMethodField() #method_name默认等于get_<field_name>
    # prop = serializers.SerializerMethodField(method_name='getProp')
    class Meta:
        model = Diagnosis
        fields = '__all__'

    def get_diagnosis_prop(self,obj):
        res = classify(os.path.join(MEDIA_ROOT, str(obj.diagnosis_image)))
        return res
    # def getProp(self,obj):
    #     # print(obj)
    #     return str(obj)

class MessagesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Messages
        fields = '__all__'