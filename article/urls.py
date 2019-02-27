# encoding=utf-8
# life is fantastic
__author__ = "Anningcsp"
# Time:2019/2/27
from django.urls import path,include,re_path
from article.views import get_all_article,post_like,sendcomment,sendforum,delet_article
urlpatterns = [
    path('get_all_article/', get_all_article),
    path('post_like/', post_like),
    path('sendcomment/',sendcomment),
    path('sendforum/',sendforum),
    path('delet_article/',delet_article),
]