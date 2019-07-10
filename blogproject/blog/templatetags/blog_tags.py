from django import template
from django.db.models.aggregates import Count
from django.db.models import Q

from ..models import Post, Category, Tag, Link, Series, Notice, Setting
import random
from comments.models import Comment

register = template.Library()


@register.simple_tag
def get_posts_pic():
    """
    生成文章图片列表，每个文章随机显示
    图片在./blog/static/blog/images中
    """
    try:
        pic_num = Setting.objects.get().post_pic
    except BaseException:
        pic_num = 1
    context_pic = ['{}.jpg'.format(x) for x in range(1, pic_num + 1)]
    return context_pic


@register.simple_tag
def get_recent_posts(num=5):
    post = Post.objects.filter(status='0').order_by('-created_time')[:num]
    return post


@register.simple_tag
def get_pop_posts(num=5):
    # return Post.objects.filter(status='0').order_by('-views')[:num]
    post = Post.objects.filter(status='0').order_by('-views')[:num].values()
    res = list()
    i = 1
    for r in post:
        if i == 1:
            r['bg_color'] = "#fd8c84"
        elif i == 2:
            r['bg_color'] = "#6fc299"
        elif i == 3:
            r['bg_color'] = "#81c1f2"
        elif i == 4:
            r['bg_color'] = "#ffd700"
        elif i == 5:
            r['bg_color'] = "#999999"
        else:
            r['bg_color'] = "#999999"
        res.append(r)
        i += 1
    return res


@register.simple_tag
def get_like_posts(post_id, num, category, tags=None, series=None):   # 猜你喜欢，首先是查系列，然后是标签，再是分类，最后是阅读数最多是
    res = list()
    all_id = list()
    
    if series:
        series_post = Post.objects.exclude(id=post_id).filter(status='0', series_id=series).order_by('-views')[:num].values()
        for r in series_post:
            res.append(r)
            all_id.append(r['id'])
    
    if tags:
        tags_post = Post.objects.exclude(id=post_id).filter(status='0', tags__id__in=tags.split(',')).distinct().order_by('-views')[:num].values()
        for r in tags_post:
            if r['id'] in all_id:
                continue
            res.append(r)
            all_id.append(r['id'])
    
    if len(res) < num:
        if category:
            category_post = Post.objects.exclude(id=post_id).filter(status='0', category_id=category).order_by('-views')[:num - len(res)].values()
        for r in category_post:
            if r['id'] in all_id:
                continue
            res.append(r)
            all_id.append(r['id'])
    
    if len(res) < num:
        post = Post.objects.exclude(id=post_id).filter(status='0').order_by('-views')[:num - len(res)].values()
        for r in post:
            if r['id'] in all_id:
                continue
            res.append(r)
            all_id.append(r['id'])
    
    res_fin = list()
    i = 1
    for r in res:
        if i == 1:
            r['bg_color'] = "#fd8c84"
        elif i == 2:
            r['bg_color'] = "#6fc299"
        elif i == 3:
            r['bg_color'] = "#81c1f2"
        elif i == 4:
            r['bg_color'] = "#ffd700"
        elif i == 5:
            r['bg_color'] = "#999999"
        else:
            r['bg_color'] = "#999999"
        res_fin.append(r)
        i += 1
    return res_fin
    
    
@register.simple_tag
def get_like_posts_tags(post_id, num, category, tags=None):   # 猜你喜欢，首先是查系列，然后是标签，再是分类，最后是阅读数最多是
    res = list()
    all_id = list()
    
    if tags:
        tags_post = Post.objects.exclude(id=post_id).filter(status='0', tags__id__in=tags.split(',')).distinct().order_by('-views')[:num].values()
        for r in tags_post:
            res.append(r)
            all_id.append(r['id'])
    
    if len(res) < num:
        if category:
            category_post = Post.objects.exclude(id=post_id).filter(status='0', category_id=category).order_by('-views')[:num - len(res)].values()
        for r in category_post:
            if r['id'] in all_id:
                continue
            res.append(r)
            all_id.append(r['id'])
    
    if len(res) < num:
        post = Post.objects.exclude(id=post_id).filter(status='0').order_by('-views')[:num - len(res)].values()
        for r in post:
            if r['id'] in all_id:
                continue
            res.append(r)
            all_id.append(r['id'])
    
    res_fin = list()
    i = 1
    for r in res:
        if i == 1:
            r['bg_color'] = "#fd8c84"
        elif i == 2:
            r['bg_color'] = "#6fc299"
        elif i == 3:
            r['bg_color'] = "#81c1f2"
        elif i == 4:
            r['bg_color'] = "#ffd700"
        elif i == 5:
            r['bg_color'] = "#999999"
        else:
            r['bg_color'] = "#999999"
        res_fin.append(r)
        i += 1
    return res_fin


@register.simple_tag
def get_like_posts_series(post_id, num, category, series=None):   # 猜你喜欢，首先是查系列，然后是标签，再是分类，最后是阅读数最多是
    res = list()
    all_id = list()
    
    if series:
        series_post = Post.objects.exclude(id=post_id).filter(status='0', series_id=series).order_by('-views')[:num].values()
        for r in series_post:
            res.append(r)
            all_id.append(r['id'])
    
    if len(res) < num:
        if category:
            category_post = Post.objects.exclude(id=post_id).filter(status='0', category_id=category).order_by('-views')[:num - len(res)].values()
        for r in category_post:
            if r['id'] in all_id:
                continue
            res.append(r)
            all_id.append(r['id'])
    
    if len(res) < num:
        post = Post.objects.exclude(id=post_id).filter(status='0').order_by('-views')[:num - len(res)].values()
        for r in post:
            if r['id'] in all_id:
                continue
            res.append(r)
            all_id.append(r['id'])
    
    res_fin = list()
    i = 1
    for r in res:
        if i == 1:
            r['bg_color'] = "#fd8c84"
        elif i == 2:
            r['bg_color'] = "#6fc299"
        elif i == 3:
            r['bg_color'] = "#81c1f2"
        elif i == 4:
            r['bg_color'] = "#ffd700"
        elif i == 5:
            r['bg_color'] = "#999999"
        else:
            r['bg_color'] = "#999999"
        res_fin.append(r)
        i += 1
    return res_fin


@register.simple_tag
def archives():
    return Post.objects.filter(status='0').dates('created_time', 'month', order='DESC')


@register.simple_tag
def archives_date(year, month):
    return Post.objects.filter(status='0',
                               created_time__year=year,
                               created_time__month=month,
                               ).count()


@register.simple_tag
def get_link():
    return Link.objects.all()


@register.simple_tag
def get_categories():
    # 记得在顶部引入 count 函数
    # return Category.objects.all()
    # 这里 annotate 不仅从数据库获取了全部分类，相当于使用了 all 方法，它还帮我们为每一个分类添加了一个 num_posts 属性
    return Category.objects.filter(post__status='0').annotate(num_posts=Count('post')).filter(num_posts__gt=0)


@register.simple_tag
def get_tags():
    # 记得在顶部引入 Tag model
    # return Tag.objects.filter(post__status='0').annotate(num_posts=Count('post')).filter(num_posts__gt=0)
    tag = Tag.objects.filter(post__status='0').annotate(num_posts=Count('post')).filter(num_posts__gt=0).values()
    res = list()
    bg = ["primary", "secondary", "success", "dark", "alert", "warning", "yellow", "default"]
    size = ["mini", "small", "large", " "]
    for i in tag:
        i["bg_color"] = random.choice(bg)
        i["size"] = random.choice(size)
        res.append(i)
    return res


@register.simple_tag
def get_series():
    return Series.objects.filter(post__status='0').annotate(num_posts=Count('post')).filter(num_posts__gt=0)


@register.simple_tag
def get_notice(num=5):
    return Notice.objects.filter(status='0')[:num]

