from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.html import strip_tags, format_html
import markdown
from mdeditor.fields import MDTextField


class Base(models.Model):   # 基类模型
    name = models.CharField(max_length=32, unique=True, verbose_name='名称')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')

    def __str__(self):
        return self.name

    class Meta:
        abstract = True
        ordering = ['-created_time']


class Series(Base):
    class Meta:
        verbose_name = '文章系列'
        verbose_name_plural = '文章系列'    # 复数形式


class Category(Base):
    class Meta:
        verbose_name = '文章分类'
        verbose_name_plural = '文章分类'


class Tag(Base):
    class Meta:
        verbose_name = '文章标签'
        verbose_name_plural = '文章标签'


class Link(Base):
    url = models.URLField(unique=True, verbose_name='地址URL')
    description = models.CharField(max_length=255, default='没有添加描述', verbose_name='描述')

    class Meta:
        verbose_name = '友情链接'
        verbose_name_plural = '友情链接'


class Post(models.Model):
    """
    文章的数据库表稍微复杂一点，主要是涉及的字段更多。
    """
    STATUS_CHOICES = (
        ('0', '发布'),
        ('1', '存稿'),
    )
    CATEGORYS_CHOICES = (
        ('0', '原创'),
        ('1', '转载'),
    )
    
    COMMENT_CHOICES = (
        (0, '可评论'),
        (1, '不可评论'),
    )

    # 文章标题
    title = models.CharField(max_length=70, verbose_name='标题', unique=True)

    # 文章正文，我们使用了 TextField。
    # 存储比较短的字符串可以使用 CharField，但对于文章的正文来说可能会是一大段文本，因此使用 TextField 来存储大段文本。
    # body = models.TextField(verbose_name='内容')
    body = MDTextField(verbose_name='内容')

    # 这两个列分别表示文章的创建时间和最后一次修改时间，存储时间的字段用 DateTimeField 类型。
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')
    modified_time = models.DateTimeField(auto_now=True, verbose_name='修改时间')

    # 文章摘要，可以没有文章摘要，但默认情况下 CharField 要求我们必须存入数据，否则就会报错。
    # 指定 CharField 的 blank=True 参数值后就可以允许空值了。
    excerpt = models.CharField(max_length=200, blank=True, verbose_name='预览', help_text='可为空')

    # 这是分类与标签，分类与标签的模型我们已经定义在上面。
    # 我们在这里把文章对应的数据库表和分类、标签对应的数据库表关联了起来，但是关联形式稍微有点不同。
    # 我们规定一篇文章只能对应一个分类，但是一个分类下可以有多篇文章，所以我们使用的是 ForeignKey，即一对多的关联关系。
    # 而对于标签来说，一篇文章可以有多个标签，同一个标签下也可能有多篇文章，所以我们使用 ManyToManyField，表明这是多对多的关联关系。
    # 同时我们规定文章可以没有标签，因此为标签 tags 指定了 blank=True。
    # 如果你对 ForeignKey、ManyToManyField 不了解，请看教程中的解释，亦可参考官方文档：
    # https://docs.djangoproject.com/en/2.2.3/topics/db/models/#relationships
    # 2.0 后必须指定 on_delete，这里指定 models.CASCADE 表示，如果删除分类，则此分类下的文章也一并删除
    category = models.ForeignKey(Category, verbose_name='分类', on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag, blank=True, verbose_name='标签')

    # 文章作者，这里 User 是从 django.contrib.auth.models 导入的。
    # django.contrib.auth 是 Django 内置的应用，专门用于处理网站用户的注册、登录等流程，User 是 Django 为我们已经写好的用户模型。
    # 这里我们通过 ForeignKey 把文章和 User 关联了起来。
    # 因为我们规定一篇文章只能有一个作者，而一个作者可能会写多篇文章，因此这是一对多的关联关系，和 Category 类似。
    author = models.ForeignKey(User, verbose_name='作者', on_delete=models.CASCADE)

    # 新增 views 字段记录阅读量
    views = models.PositiveIntegerField(default=0, editable=False, verbose_name='阅读量')

    status = models.CharField(default=0, max_length=1, choices=STATUS_CHOICES, verbose_name='状态')      # 发布状态
    categorys = models.CharField(default=0, max_length=1, choices=CATEGORYS_CHOICES, verbose_name='类型')
    series = models.ForeignKey(Series, verbose_name='系列', null=True, blank=True, help_text='可为空', on_delete=models.CASCADE)        # 系列
    
    comment_status = models.SmallIntegerField(default=0, choices=COMMENT_CHOICES, verbose_name='评论状态')      # 评论状态

    def __str__(self):
        return self.title

    def colored_status(self):   # 自定义字段在admin后台显示
        if self.status == '1':
            color_code = 'red'
            return format_html('<span style="color: {};">{}</span>', color_code, '存稿')
        else:
            return format_html('<span>{}</span>', '发布')

    colored_status.short_description = "状态"
    colored_status.admin_order_field = 'created_time'   # 排序字段

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'pk': self.pk})
    
    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    def save(self, *args, **kwargs):    
        # 如果没有填写摘要
        if not self.excerpt:
            # 首先实例化一个 Markdown 类，用于渲染 body 的文本
            md = markdown.Markdown(extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ])
            # 先将 Markdown 文本渲染成 HTML 文本
            # strip_tags 去掉 HTML 文本的全部 HTML 标签
            # 从文本摘取前 54 个字符赋给 excerpt
            self.excerpt = strip_tags(md.convert(self.body))[:54]

        # 调用父类的 save 方法将数据保存到数据库中
        super(Post, self).save(*args, **kwargs)
        
    class Meta:
        verbose_name = '文章'
        verbose_name_plural = '文章'
        ordering = ['-created_time']


class Notice(models.Model):
    STATUS_CHOICES = (
        ('0', '显示'),
        ('1', '不显示'),
    )
    
    content = models.CharField(max_length=100, unique=True, verbose_name='内容')
    add_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')
    status = models.CharField(default=0, max_length=1, choices=STATUS_CHOICES, verbose_name='是否显示')
    
    def __str__(self):
        return self.content

    class Meta:
        verbose_name = '公告'
        verbose_name_plural = '公告'
        ordering = ['-add_time']


class Setting(models.Model):
    # body = models.TextField('博主信息', )
    body = MDTextField(verbose_name='博主信息')
    pages = models.SmallIntegerField('分页数', default=5)
    post_pic = models.SmallIntegerField('文章随机图片', default=1)
    
    def __str__(self):
        return self.body

    class Meta:
        verbose_name = '设置'
        verbose_name_plural = '设置'

