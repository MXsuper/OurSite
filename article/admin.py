from django.contrib import admin
from .models import Article,Comment_nums,Comment,Reply,Likes,Likes_count
# Register your models here.
admin.site.register(Article)
admin.site.register(Comment_nums)
admin.site.register(Comment)
admin.site.register(Reply)
admin.site.register(Likes)
admin.site.register(Likes_count)
