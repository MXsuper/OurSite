from django.contrib import admin
from .models import Article,Comment,Reply,Likes,Collection
# Register your models here.
admin.site.register(Article)
admin.site.register(Comment)
admin.site.register(Reply)
admin.site.register(Likes)
admin.site.register(Collection)
