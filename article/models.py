from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from DjangoUeditor.models import UEditorField #头部增加这行代码导入UEditorField

# 文章
class Article(models.Model):
    title = models.CharField('标题', max_length=70)
    excerpt = models.TextField('摘要', max_length=200, blank=True)
    """ 保留字段，可扩展。"""
    #category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, verbose_name='分类', blank=True, null=True)
    # 使用外键关联分类表与分类是一对多关系
    #tags = models.ManyToManyField(Tag, verbose_name='标签', blank=True)
    # 使用外键关联标签表与标签是多对多关系

    # 存储文章展示时候的缩略图
    img = models.ImageField(upload_to='article_img/%Y/%m/%d/', verbose_name='文章图片', blank=True, null=True)
    """
    富文档启用
    body = UEditorField('内容', width=800, height=500,
                        toolbars="full", imagePath="upimg/", filePath="upfile/",
                        upload_settings={"imageMaxSize": 1204000},
                        settings={}, command=None, blank=True
                        )
    # TODO（anning) : 使用富文本编辑器可能会导致django报错  \
    # F:\course\myblog\myblogvenv\lib\site-packages\django\forms\boundfield.py in as_widget, line 93
    # 那么只需要打开boundfield.py 注释掉renderer = self.form.renderer
    
    """
    body = models.TextField(verbose_name="文章内容",max_length=200)


    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='作者')

    """
    由于暂时没有user这个类，所以先调用原装的user
    文章作者，这里User是从django.contrib.auth.models导入的。
    这里我们通过 ForeignKey 把文章和 User 关联了起来。
    """
    views = models.PositiveIntegerField('阅读量', default=0)
    created_time = models.DateTimeField('发布时间', auto_now_add=True)
    modified_time = models.DateTimeField('修改时间', auto_now=True)
    like_count = models.PositiveIntegerField("总点赞人数", default=0)
    count_comment = models.PositiveIntegerField('总评论数',default=0)

class Comment(models.Model):
    """
    评论表，只记录评论内容，然后用一个reply表来记录信息，topic_type 记录是否为根评论，1为是，2为否
    """
    article_id = models.ForeignKey(Article,on_delete=models.CASCADE,verbose_name='文章id')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='评论人')
    content = models.TextField('评论内容',max_length=100,blank=False)
    topic_type = models.IntegerField('评论类型',default=1) # 1表示评论，2表示回复
    comment_time = models.DateTimeField('评论时间', auto_now_add=True)

class Reply(models.Model):
    """
    评论回复，构成一颗树，检索父子节点，即可以得知评论的顺序
    """
    parent_id = models.ForeignKey(Comment,related_name='parent_id', on_delete=models.CASCADE, verbose_name='父')
    child_id = models.ForeignKey(Comment,related_name='child_id', on_delete=models.CASCADE, verbose_name='子')



class Likes(models.Model):
    """
    用于点赞唯一，记录点赞人的信息
    """
    article_id = models.ForeignKey(Article,on_delete=models.CASCADE,verbose_name='文章id')
    user_id = models.ForeignKey(User,on_delete=models.CASCADE, verbose_name='点赞人')
