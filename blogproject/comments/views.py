from django.shortcuts import render, get_object_or_404, redirect
from blog.models import Post
from .models import Comment
from .forms import CommentForm, CommentFormCode
import markdown
from django.conf import settings
from django.http import HttpResponse, JsonResponse, Http404
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import re
from PIL import Image, ImageDraw, ImageFont
import random
from io import BytesIO
from datetime import datetime, timedelta, timezone


# 确定重复是否重复
def confirm(text, name, post_id):
    res = Comment.objects.filter(text=text, name=name, post_id=post_id)
    if res:
        return False
    else:
        return True


def post_comment_old(request, post_pk):
    # 先获取被评论的文章，因为后面需要把评论和被评论的文章关联起来。
    # 这里我们使用了 Django 提供的一个快捷函数 get_object_or_404，
    # 这个函数的作用是当获取的文章（Post）存在时，则获取；否则返回 404 页面给用户。
    post = get_object_or_404(Post, pk=post_pk)

    if post.status == '1':
        raise Http404("post does not exist")

    md = markdown.Markdown(extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
    ])
    post.body = md.convert(post.body)
    post.toc = md.toc
#    post.body = markdown.markdown(post.body,
#                              extensions=[
#                                 'markdown.extensions.extra',
#                                 'markdown.extensions.codehilite',
#                                 'markdown.extensions.toc',
#                              ])

    # HTTP 请求有 get 和 post 两种，一般用户通过表单提交数据都是通过 post 请求，
    # 因此只有当用户的请求为 post 时才需要处理表单数据。
    if request.method == 'POST':
        # 用户提交的数据存在 request.POST 中，这是一个类字典对象。
        # 我们利用这些数据构造了 CommentForm 的实例，这样 Django 的表单就生成了。
        form = CommentForm(request.POST)

        # 当调用 form.is_valid() 方法时，Django 自动帮我们检查表单的数据是否符合格式要求。
        if form.is_valid():
            # 检查到数据是合法的，调用表单的 save 方法保存数据到数据库，
            # commit=False 的作用是仅仅利用表单的数据生成 Comment 模型类的实例，但还不保存评论数据到数据库。
            comment = form.save(commit=False)

            # 将评论和被评论的文章关联起来。
            comment.post = post

            # 最终将评论数据保存进数据库，调用模型实例的 save 方法
            comment.save()

            # 重定向到 post 的详情页，实际上当 redirect 函数接收一个模型的实例时，它会调用这个模型实例的 get_absolute_url 方法，
            # 然后重定向到 get_absolute_url 方法返回的 URL。
            return redirect(post)

        else:
            # 检查到数据不合法，重新渲染详情页，并且渲染表单的错误。
            # 因此我们传了三个模板变量给 detail.html，
            # 一个是文章（Post），一个是评论列表，一个是表单 form
            # 注意这里我们用到了 post.comment_set.all() 方法，
            # 这个用法有点类似于 Post.objects.all()
            # 其作用是获取这篇 post 下的的全部评论，
            # 因为 Post 和 Comment 是 ForeignKey 关联的，
            # 因此使用 post.comment_set.all() 反向查询全部评论。
            # 具体请看下面的讲解。
            comment_list = post.comment_set.all()

            has_prev = False
            has_next = False
            id_active = post.id

            prev_post = Post.objects.filter(status='0', id__lt=id_active).order_by('-id').first()
            if prev_post:
                has_prev = True

            next_post = Post.objects.filter(status='0', id__gt=id_active).order_by('id').first()
            if next_post:
                has_next = True

            context = {'post': post,
                       'form': form,
                       'comment_list': comment_list,
                       'has_prev': has_prev,
                       'has_next': has_next,
                       'prev_post': prev_post,
                       'next_post': next_post,
                       }
            return render(request, 'blog/detail.html', context=context)
    # 不是 post 请求，说明用户没有提交数据，重定向到文章详情页。
    return redirect(post)


def post_comment(request, post_pk):
    # 先获取被评论的文章，因为后面需要把评论和被评论的文章关联起来。
    # 这里我们使用了 Django 提供的一个快捷函数 get_object_or_404，
    # 这个函数的作用是当获取的文章（Post）存在时，则获取；否则返回 404 页面给用户。
    post = get_object_or_404(Post, pk=post_pk)

    if post.status == '1':
        raise Http404("post does not exist")
        
        
    if post.comment_status == 1:
        return JsonResponse({"code": 400, "err": "不可评论"})
        
        
    # HTTP 请求有 get 和 post 两种，一般用户通过表单提交数据都是通过 post 请求，
    # 因此只有当用户的请求为 post 时才需要处理表单数据。
    if request.method == 'POST':
        # 用户提交的数据存在 request.POST 中，这是一个类字典对象。
        # 我们利用这些数据构造了 CommentForm 的实例，这样 Django 的表单就生成了。
        form = CommentFormCode(request.POST)

        captcha = request.POST.get("captcha")  # 获取用户填写的验证码
        if captcha and captcha.upper() == request.session.get("captcha", "").upper():
            # 当调用 form.is_valid() 方法时，Django 自动帮我们检查表单的数据是否符合格式要求。
            if form.is_valid():
                # 验证后的表单数据在 form.cleaned_data 中以字典形式存放
                if confirm(form.cleaned_data['text'], form.cleaned_data['name'], post.id):
                    # 检查到数据是合法的，调用表单的 save 方法保存数据到数据库，
                    # commit=False 的作用是仅仅利用表单的数据生成 Comment 模型类的实例，但还不保存评论数据到数据库。
                    comment = form.save(commit=False)

                    # 将评论和被评论的文章关联起来。
                    comment.post = post

                    # 最终将评论数据保存进数据库，调用模型实例的 save 方法
                    comment.save()
                    get_captcha(request)    # 提交后不管成功与否都重新生成一次验证码，防止暴力破解不断重试一个验证码
                    return JsonResponse({"code": 200, "err": "评论成功"})
                else:
                    get_captcha(request)
                    return JsonResponse({"code": 401, "err": "重复的评论"})
            else:
                get_captcha(request)
                return JsonResponse({"code": 402, "err": "错误的评论内容"})
        else:
            get_captcha(request)
            return JsonResponse({"code": 403, "err": "错误的验证码"})
    
    # 不是 post 请求，说明用户没有提交数据，重定向到文章详情页。
    get_captcha(request)
    return JsonResponse({"code": 405, "err": "方法不允许"})


# 获取评论，前端使用 ajax
def get_comment(request, post_pk):
    page_num = request.GET.get('page', '1')
    num = 10
    post = get_object_or_404(Post, pk=post_pk)
    if post.status == '1':
        raise Http404("post does not exist")
    
    page_num = int(page_num)
    if page_num <= 0:
        page_num = 1
    
    comment_list = Comment.objects.filter(post_id=post_pk).values()[(page_num - 1) * num:page_num * num]
    
    lists = []
    for i in comment_list:
        # django 底层存储的是 UTC 时间，需转换
        i['created_time'] = i['created_time'].astimezone(timezone(timedelta(hours=8))).strftime(u"%Y年%m月%d日 %H:%M".encode('gbk').decode('latin-1')).encode('latin-1').decode('gbk')
        lists.append(i)

    has_next = 1
    if len(lists) < num:
        has_next = 0

    return JsonResponse({"code": 200, "page_num": page_num, "lists": lists, "has_next": has_next})


# 获取验证码图片的视图
def get_captcha(request):
    # 获取随机颜色的函数
    def get_random_color():
        return random.randint(220, 255), random.randint(220, 255), random.randint(220, 255)

    def get_random_color_font():
        return random.randint(30, 180), random.randint(30, 180), random.randint(30, 180)

    # 生成一个图片对象
    img_obj = Image.new(
        'RGB',
        (200, 35),
        get_random_color()
    )
    # 在生成的图片上写字符
    # 生成一个图片画笔对象
    draw_obj = ImageDraw.Draw(img_obj)
    # 加载字体文件， 得到一个字体对象
    # font_obj = ImageFont.truetype("static/font/kumo.ttf", 28)
    font_obj = ImageFont.truetype("consola.ttf", 45)  # 设置字体
    # 开始生成随机字符串并且写到图片上
    tmp_list = []
    for i in range(5):
        u = chr(random.randint(65, 90))  # 生成大写字母
        l = chr(random.randint(97, 122))  # 生成小写字母
        n = str(random.randint(0, 9))  # 生成数字，注意要转换成字符串类型

        tmp = random.choice([u, l, n])
        tmp_list.append(tmp)
        draw_obj.text((10 + 40 * i, random.randint(0, 5)), tmp, fill=get_random_color_font(), font=ImageFont.truetype("consola.ttf", random.randint(25, 45)))
        # draw_obj.text((10 + 40 * i, 0), tmp, fill=get_random_color_font(), font=font_obj)
        # draw_obj.text((20 + 40 * i, 0), tmp, fill=get_random_color())

    # 保存到session
    request.session["captcha"] = "".join(tmp_list)
    request.session.set_expiry(1800)    # session 失效时间1800s
    
    # 加干扰线
    width = 200  # 图片宽度（防止越界）
    height = 35
    for i in range(5):
        x1 = random.randint(0, width)
        x2 = random.randint(0, width)
        y1 = random.randint(0, height)
        y2 = random.randint(0, height)
        draw_obj.line((x1, y1, x2, y2), fill=get_random_color_font())

    # 加干扰点
    for i in range(40):
        draw_obj.point((random.randint(0, width), random.randint(0, height)), fill=get_random_color_font())
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw_obj.arc((x, y, x+4, y+4), 0, 90, fill=get_random_color_font())

    # 不需要在硬盘上保存文件，直接在内存中加载就可以
    io_obj = BytesIO()
    # 将生成的图片数据保存在io对象中
    img_obj.save(io_obj, "png")
    # 从io对象里面取上一步保存的数据
    data = io_obj.getvalue()
    return HttpResponse(data)


# 获取验证码图片的视图
def get_captcha_admin(request):
    # 获取随机颜色的函数
    def get_random_color():
        return random.randint(220, 255), random.randint(220, 255), random.randint(220, 255)

    def get_random_color_font():
        return random.randint(30, 180), random.randint(30, 180), random.randint(30, 180)

    # 生成一个图片对象
    img_obj = Image.new(
        'RGB',
        (200, 35),
        get_random_color()
    )
    # 在生成的图片上写字符
    # 生成一个图片画笔对象
    draw_obj = ImageDraw.Draw(img_obj)
    # 加载字体文件， 得到一个字体对象
    # font_obj = ImageFont.truetype("static/font/kumo.ttf", 28)
    font_obj = ImageFont.truetype("consola.ttf", 45)  # 设置字体
    # 开始生成随机字符串并且写到图片上
    tmp_list = []
    for i in range(5):
        u = chr(random.randint(65, 90))  # 生成大写字母
        l = chr(random.randint(97, 122))  # 生成小写字母
        n = str(random.randint(0, 9))  # 生成数字，注意要转换成字符串类型

        tmp = random.choice([u, l, n])
        tmp_list.append(tmp)
        draw_obj.text((10 + 40 * i, random.randint(0, 5)), tmp, fill=get_random_color_font(), font=ImageFont.truetype("consola.ttf", random.randint(25, 45)))
        # draw_obj.text((10 + 40 * i, 0), tmp, fill=get_random_color_font(), font=font_obj)
        # draw_obj.text((20 + 40 * i, 0), tmp, fill=get_random_color())

    # 保存到session
    request.session["captcha_admin"] = "".join(tmp_list)
    request.session.set_expiry(600)    # session 失效时间1800s
    
    # 加干扰线
    width = 200  # 图片宽度（防止越界）
    height = 35
    for i in range(5):
        x1 = random.randint(0, width)
        x2 = random.randint(0, width)
        y1 = random.randint(0, height)
        y2 = random.randint(0, height)
        draw_obj.line((x1, y1, x2, y2), fill=get_random_color_font())

    # 加干扰点
    for i in range(40):
        draw_obj.point((random.randint(0, width), random.randint(0, height)), fill=get_random_color_font())
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw_obj.arc((x, y, x+4, y+4), 0, 90, fill=get_random_color_font())

    # 不需要在硬盘上保存文件，直接在内存中加载就可以
    io_obj = BytesIO()
    # 将生成的图片数据保存在io对象中
    img_obj.save(io_obj, "png")
    # 从io对象里面取上一步保存的数据
    data = io_obj.getvalue()
    return HttpResponse(data)

