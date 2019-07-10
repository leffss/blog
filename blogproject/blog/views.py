from django.shortcuts import render, get_object_or_404
from django.http import Http404, HttpResponse, JsonResponse
from .models import Post, Category, Tag, Setting, Series
from comments.forms import CommentForm
from django.views.generic import ListView, DetailView
from django.db.models import Q
import markdown
from pure_pagination import PaginationMixin
# Create your views here.
from haystack.generic_views import SearchView


def index(request):
    post_list = Post.objects.filter(status='0')
    return render(request, 'blog/index.html', context={'post_list': post_list})


def detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    
    if post.status == '1':
        raise Http404("post does not exist")

    # 阅读量 +1
    post.increase_views()

    post.body = markdown.markdown(post.body,
                                  extensions=[
                                     'markdown.extensions.extra',
                                     'markdown.extensions.codehilite',
                                     'markdown.extensions.toc',
                                  ])
    # 记得在顶部导入 CommentForm
    form = CommentForm()
    # 获取这篇 post 下的全部评论
    comment_list = post.comment_set.all()

    # 将文章、表单、以及文章下的评论列表作为模板变量传给 detail.html 模板，以便渲染相应数据。
    context = {'post': post,
               'form': form,
               'comment_list': comment_list
               }
    return render(request, 'blog/detail.html', context={'post': post})


def archives(request, year, month):
    post_list = Post.objects.filter(created_time__year=year,
                                    created_time__month=month,
                                    status='0'
                                    )
    return render(request, 'blog/index.html', context={'post_list': post_list})


def category(request, pk):
    cate = get_object_or_404(Category, pk=pk)
    post_list = Post.objects.filter(category=cate, status='0')
    return render(request, 'blog/index.html', context={'post_list': post_list})


class IndexView(PaginationMixin, ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    try:
        pages = Setting.objects.get().pages
    except BaseException:
        pages = 5
    paginate_by = pages

    def get_queryset(self):
        qs = super().get_queryset()  # 调用父类方法
        return qs.filter(status='0')


class MySearchView(PaginationMixin, SearchView):
    template_name = 'blog/search.html'
    context_object_name = "post_list"
    try:
        pages = Setting.objects.get().pages
    except BaseException:
        pages = 5
    paginate_by = pages
    # queryset = SearchQuerySet().order_by('-views')

    def get_queryset(self):
        queryset = super().get_queryset()
        # return queryset.filter(status='0')
        return queryset.order_by('-views')  # 排序

    def get_context_data(self, *args, **kwargs):
        # context = super(MySearchView, self).get_context_data(*args, **kwargs)
        context = super(MySearchView, self).get_context_data(**kwargs)
        # 定义文章图片,模板中每个文章随机显示
        context_pic = ['{}.jpg'.format(x) for x in range(1, 51)]
        context.update({
            'context_pic': context_pic,
            'page_title': "搜索",
        })
        return context
        
        
class CategoryView(IndexView):
    template_name = 'blog/archive.html'

    def get_queryset(self):
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super(CategoryView, self).get_queryset().filter(category=cate)
        
    def get_context_data(self, **kwargs):
        context = super(CategoryView, self).get_context_data(**kwargs)
        category_name = Category.objects.filter(pk=self.kwargs.get('pk')).values()
        context.update({
            'page_title': "分类",
            'archive_name': category_name[0]['name'],
        })
        return context
        
                                         
class TagView(IndexView):
    template_name = 'blog/archive.html'

    def get_queryset(self):
        tag = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return super(TagView, self).get_queryset().filter(tags=tag, status='0')
    
    def get_context_data(self, **kwargs):
        context = super(TagView, self).get_context_data(**kwargs)
        tag_name = Tag.objects.filter(pk=self.kwargs.get('pk')).values()
        print(tag_name)
        context.update({
            'page_title': "标签",
            'archive_name': tag_name[0]['name'],
        })
        return context
        
        
class SeriesView(IndexView):
    template_name = 'blog/archive.html'

    def get_queryset(self):
        series = get_object_or_404(Series, pk=self.kwargs.get('pk'))
        return super(SeriesView, self).get_queryset().filter(series=series)
    
    def get_context_data(self, **kwargs):
        context = super(SeriesView, self).get_context_data(**kwargs)
        series_name = Series.objects.filter(pk=self.kwargs.get('pk')).values()
        context.update({
            'page_title': "系列",
            'archive_name': series_name[0]['name'],
        })
        return context
        
        
class ArchivesView(IndexView):
    template_name = 'blog/archive.html'

    def get_queryset(self):
        return super(ArchivesView, self).get_queryset().filter(created_time__year=self.kwargs.get('year'),
                                                                created_time__month=self.kwargs.get('month'),
                                                               )

    def get_context_data(self, **kwargs):
        context = super(ArchivesView, self).get_context_data(**kwargs)
        context.update({
            'page_title': "归档",
            'archive_name': "{0} 年 {1} 月".format(self.kwargs.get('year'), self.kwargs.get('month')),
        })
        return context
        

class PostDetailView(DetailView):
    # 这些属性的含义和 ListView 是一样的
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        # 覆写 get 方法的目的是因为每当文章被访问一次，就得将文章阅读量 +1
        # get 方法返回的是一个 HttpResponse 实例
        # 之所以需要先调用父类的 get 方法，是因为只有当 get 方法被调用后，
        # 才有 self.object 属性，其值为 Post 模型实例，即被访问的文章 post
        response = super(PostDetailView, self).get(request, *args, **kwargs)
        
        if self.object.status == '1':
            raise Http404("post does not exist")
        
        # 将文章阅读量 +1
        # 注意 self.object 的值就是被访问的文章 post
        self.object.increase_views()

        # 视图必须返回一个 HttpResponse 对象
        return response

    def get_object(self, queryset=None):
        # 覆写 get_object 方法的目的是因为需要对 post 的 body 值进行渲染
        post = super(PostDetailView, self).get_object(queryset=None)
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
        ])
        post.body = md.convert(post.body)
        post.toc = md.toc
        return post

    def get_context_data(self, **kwargs):
        # 覆写 get_context_data 的目的是因为除了将 post 传递给模板外（DetailView 已经帮我们完成），
        # 还要把评论表单、post 下的评论列表传递给模板。
        context = super(PostDetailView, self).get_context_data(**kwargs)
        form = CommentForm()
        # 获取 5 条评论，更多的使用 ajax 获取
        num = 10
        comment_list = self.object.comment_set.all()[0:num]
        has_next_comment = True
        if len(comment_list) < num:
            has_next_comment = False

        has_prev = False
        has_next = False
        id_active = self.object.id

        prev_post = Post.objects.filter(status='0', id__lt=id_active).order_by('-id').first()
        if prev_post:
            has_prev = True

        next_post = Post.objects.filter(status='0', id__gt=id_active).order_by('id').first()
        if next_post:
            has_next = True

        post = super(PostDetailView, self).get_object(queryset=None)
        tags = [str(i.id) for i in post.tags.all()]
                
        context.update({
            'form': form,
            'comment_list': comment_list,
            'has_prev': has_prev,
            'has_next': has_next,
            'has_next_comment': has_next_comment,
            'prev_post': prev_post,
            'next_post': next_post,
            'post_tags': ','.join(tags),
        })
        return context
       

def search(request):
    q = request.GET.get('q')
    error_msg = ''

    if not q:
        error_msg = "请输入关键词"
        return render(request, 'blog/index.html', {'error_msg': error_msg})

    post_list = Post.objects.filter(Q(title__icontains=q) | Q(body__icontains=q), status='0')
    return render(request, 'blog/index.html', {'error_msg': error_msg,
                                               'post_list': post_list})


class ArchivesallView(ListView):
    model = Post
    template_name = 'blog/archives.html'
    context_object_name = 'post_list'

    def get_queryset(self):
        qs = super().get_queryset()  # 调用父类方法
        return qs.filter(status='0')


def about(request):
    try:
        setting = Setting.objects.get().body
    except BaseException:
        setting = ''
    setting = markdown.markdown(setting,
                              extensions=[
                                 'markdown.extensions.extra',
                                 'markdown.extensions.codehilite',
                                 'markdown.extensions.toc',
                              ])
    # return render(request, 'blog/about.html', context={'setting': setting})
    return JsonResponse({'setting': setting})
