"""
-------------------------------------------------
   Author :        lin
   date：          2019/2/27 16:55
-------------------------------------------------
"""
__author__ = 'lin'

from . import views
from django.urls import path, re_path,include
from rest_framework.routers import DefaultRouter

# 创建路由器并注册视图
router = DefaultRouter()
router.register('hospital', views.HospitalViewSet, base_name='hospital')
router.register('diagnosis', views.DiagnosisViewSet, base_name='diagnosis')
router.register(r'areas', views.AreasViewSet, base_name='areas')
# router.register('areas', views.AreasViewSet, base_name='areas')
# router.register('province', views.ProvinceViewSet, base_name='province')
# router.register('areas', views.AreaViewSet, base_name='areas')

app_name = 'medical'
urlpatterns = [
    path('',include(router.urls)),
]


