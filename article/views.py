from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.http import HttpResponseBadRequest, HttpResponseForbidden,JsonResponse
from .models import Article,Likes,User,Comment,Reply,Collection
import json
from  datetime import datetime,date
from django.forms.models import model_to_dict
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
        param = json.loads(request.body)
        key = param['article_arr_type'].split('/')[0]
        type= param['article_arr_type'].split('/')[1]
        if param.get('uid'):
            print("还没有写")
            # TOKEN 认证
            #TODO: 用户获取所有的文章
        else:
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
                # TODO（ANNING）： 官方的文章接口
                return HttpResponse("你所访问的页面不存在", status=404)

    except Exception as e :
        print(e)
        return HttpResponse("获取数据失败", status=401)




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
            reply = Reply(parent_ids_id=comment_id,child_ids_id = comment.id)
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
            print("article",article_id,"has been delete","the user is ",)
        except Exception as e:
            print(e)
            return HttpResponse(status=401)
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=402)



# 添加到收藏单
@csrf_exempt
def add_to_collection(request):
    if request.method == 'POST':
        try:
            param = json.loads(request.body)
            article_id = param['article_id']
            user_id = param['user_id']
            collection = Collection.objects.get(user_id=user_id,article_id=article_id)
            if collection != None:
                return HttpResponse(status=402)
            else:
                Collection(user_id_id=user_id,article_id_id=article_id).save()
                return HttpResponse(status=200)
        except Exception as e :
            print(e)
            return HttpResponse(status=401)

    else:
        return HttpResponse(status=402)

# 删除收藏单
def delete_collections(request):
    if request.method == 'POST':
        try:
            param = json.loads(request.body)
            article_id = param['article_id']
            user_id = param['user_id']

            collection = Collection.objects.get(user_id=user_id,article_id=article_id)
            if collection == None:
                return HttpResponse(status=402)
            else:
                collection.delete()
                return HttpResponse(status=200)
        except Exception as e :
            print(e)
            return HttpResponse(status=401)
    else:
        return HttpResponse(status=402)


""" 暂停了post请求时，所需要的csrftoken，登陆后自动分配，cookie要求携带"""
@csrf_exempt
def post_like(request):
    """

    :param request:
    user_id: 当前用户的id
    article_id:当前文章的id

    :return:返回1 或者 2 ， 1表示点赞成功， 2 表示点赞取消,3 表示错误
    """


    if request.method == 'POST':
        try:
            param = json.loads(request.body)
            article_id = param['article_id']
            user_id = param['user_id']

            if article_id and user_id:
                Like = Likes.objects.filter(article_id=article_id,user_id=user_id)
                article = Article.objects.get(id=article_id)
                if Like:
                    Like.delete()
                    article.like_count = article.like_count-1 if article.like_count-1>0 else 0
                    article.save()
                    return HttpResponse(status=200,content="点赞取消")
                else:
                    Likes(article_id=article,user_id=User.objects.get(id=user_id)).save()
                    article.like_count = article.like_count+1
                    article.save()
                    return HttpResponse(status=200,content="点赞成功")
            return HttpResponseBadRequest()
        except Exception as e :
            print(e)
            return HttpResponseForbidden()

def get_reply(comment_parent_id):
    if  not Reply.objects.filter(parent_ids=comment_parent_id):
        return

    replies = Reply.objects.filter(parent_ids=comment_parent_id).values()
    all_reply = {}

    for reply in replies:

        child = Comment.objects.get(id = reply['child_ids_id'])
        time = child.comment_time
        child = model_to_dict(child)

        del child['article_id']
        del child['topic_type']

        child['time'] = time
        child['parent_id']=reply['parent_ids_id']
        child['reply']=get_reply(reply['child_ids_id'])

        all_reply[reply['child_ids_id']]=child
    return all_reply

@csrf_exempt
def get_comment_list(request):
    """
    采用树结构检索出来，因为存的时候，comment表存内容，reply表里存关系
    :param request: article_id
    :return:
    {comment_id:{
        user_id:
        user_name:
        content :
        comment_id:
        reply:{comment_id:{
                user_id:
                user_name:
                content:
                comment_id:
                parent_id:
                    reply:{
                        .......
                    }
                },
                comment_id:{
                user_id:
                user_name:
                content:
                comment_id:
                    reply:{
                        .......
                    }
                },
            }
        },
        comment_id:{
        user_id:
        user_name:
        content :
        comment_id:
        reply:{
                user_id:
                user_name:
                content:
                comment_id:
                reply:{

                }
            }
        }
    }
    """
    if request.method == 'POST':
        param = json.loads(request.body)
        param = dict(param)
        if param.get("article_id"):
            all_comment = {}
            # 首先获得所有的评论的根，然后再去检查评论有没有回复
            article_id = param.get("article_id")
            print(article_id)
            comment_root = Comment.objects.filter(topic_type=1,article_id=article_id).values()
            print(comment_root.values())
            if comment_root == None:
                return JsonResponse(all_comment)
            else:
                for comment in comment_root:

                    dic_comment = comment
                    dic_comment['reply'] = get_reply(comment['id'])
                    all_comment[comment['id']]=dic_comment

                print(all_comment)
                return JsonResponse(all_comment)
        else:
            return HttpResponseBadRequest()

    else:
        return HttpResponseBadRequest()
