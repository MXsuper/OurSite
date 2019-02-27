from django.shortcuts import render
from django.shortcuts import HttpResponse
from .models import Article,Likes,User,Comment,Reply
import json
from  datetime import datetime,date

from django.views.decorators.csrf import csrf_exempt

# Create your views here.
class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)


# 获得文章
@csrf_exempt
def get_all_article(request):
    """
    :param request:前端的article_arr_type是论坛列表的类别，/0是非官方的帖子，/1是官方的帖子，前面的hot是最多点赞，new是最新发布，pop是最受欢迎。官方的就辟谣是"piyao"、百科是"baike"
    :return: 返回点赞数最多的文章，返回的数据需要json.parser
    """

    try:
        param = json.loads(request.body)['article_arr_type']
        key = param.split('/')[0]
        type= param.split('/')[1]
        if type == '0':
            if key == 'hot':
                articles = Article.objects.all().order_by('like_count').values()
            elif key == 'pop':
                articles = Article.objects.all().order_by('count_comment').values()
            elif key == 'new':
                articles = Article.objects.all().order_by('created_time').values()
            all = {}
            for article in articles:
                article['img'] = 'http://127.0.0.1:8000/media/'+article['img']
                all[article['id']] = article
            return HttpResponse(json.dumps(all, cls=ComplexEncoder, ensure_ascii=False))
        else:
            return HttpResponse("你所访问的页面不存在", status=404)

    except Exception as e :
        print(e)
        return HttpResponse("获取数据失败", status=401)


""" 暂停了post请求时，所需要的csrftoken，登陆后自动分配，cookie要求携带"""
@csrf_exempt
def post_like(request):
    """

    :param request:
    user_id: 当前用户的id
    article_id:当前文章的id

    :return:返回1 或者 2 ， 1表示点赞成功， 2 表示点赞取消,3 表示错误
    """
    article_id = request.POST.get('article_id')
    user_id = request.POST.get('user_id')
    print(article_id,user_id)
    if article_id and user_id:
        Like = Likes.objects.filter(article_id=article_id,user_id=user_id)
        article = Article.objects.get(id=article_id)
        if Like:
            Like.delete()
            article.like_count = article.like_count-1 if article.like_count-1>0 else 0
            article.save()
            return HttpResponse("2")
        else:
            Likes(article_id=article,user_id=User.objects.get(id=user_id)).save()
            article.like_count = article.like_count+1
            article.save()
            return HttpResponse("1")
    return HttpResponse("3")


@csrf_exempt
def sendcomment(request):
    """
    发表评论或回复
    :param request:
    comment_type  : 1 表示评论，2 表示回复
    评论：
        user_id ： 评论人的id
        article_id : 文章id
        content: 评论内容
    回复：
        comment_id: 根评论的id
        user_id ： 评论人的id
        article_id : 文章id
        content: 评论内容
        reply_id: 回复人的id
    :return:
    """
    try:
        comment_type = json.loads(request.body)['comment_type']
        if comment_type == 1:
            user_id = json.loads(request.body)['user_id']
            article_id = json.loads(request.body)['article_id']
            content = json.loads(request.body)['content']
            comment = Comment(user_id= user_id,article_id_id = article_id,content = content,topic_type= comment_type)
            comment.save()
            return HttpResponse(status=200)
        elif comment_type == 2:
            user_id = json.loads(request.body)['user_id']
            article_id = json.loads(request.body)['article_id']
            content = json.loads(request.body)['content']
            comment = Comment(user_id=user_id, article_id_id=article_id, content=content, topic_type=comment_type)
            comment.save()
            comment_id = json.loads(request.body)['comment_id']
            reply = Reply(parent_id_id=comment_id,child_id_id = comment.id)
            reply.save()

            return HttpResponse(status=200)
    except Exception as e :
        print(e)
        return HttpResponse(status=402)

@csrf_exempt
def sendforum(request):
    """

    "article_title":"文章标题",
    "article_detail_content":"jiahfiwhiehegegergvavdvsdvsdvsdvsdvdvsdvsdvdsvvcsdveeveve",
    "article_simple_content":"jiahfiwhiehegegergv",
    "id":"小明"

    :param request:
    :return:
    """
    if request.method == 'POST':

        title = request.POST['article_title']
        content = request.POST['article_detail_content']
        excerpt = request.POST['article_simple_content']
        user = request.POST['id']
        try:
            Article(title=title,body=content,img = request.FILES.get('img'),excerpt=excerpt,user_id=user).save()
        except Exception as e :
            print(e)
            return HttpResponse(status=401)
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=401)


@csrf_exempt
def delet_article(request):
    """

    "id": "56a5faa",
    "article_id": "eeaojfafa23f"

    :param request:
    :return:
    """
    if request.method == 'POST':
        param = json.loads(request.body)
        article_id = param['article_id']
        # user_id = param['user_id']
        # TODO(anning) : 用户删除权限，还没写
        try:
            Article.objects.get(id=article_id).delete()
        except Exception as e:
            print(e)
            return HttpResponse(status=401)
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=402)


