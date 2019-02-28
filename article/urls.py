# encoding=utf-8
# life is fantastic
__author__ = "Anningcsp"
# Time:2019/2/27
from django.urls import path,include,re_path
from article.views import *
urlpatterns = [
    path('get_all_article/', get_all_article),
    path('post_like/', post_like),
    path('sendcomment/',sendcomment),
    path('sendforum/',sendforum),
    path('delet_article/',delet_article),
    path('add_to_collection/',add_to_collection),
    path('delete_collections/',delete_collections),
    path('get_comment_list/',get_comment_list),

]