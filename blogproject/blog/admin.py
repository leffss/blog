from django.contrib import admin
from .models import Post, Category, Tag, Series, Link, Setting, Notice
# Register your models here.


admin.site.site_title = "后台管理"
admin.site.site_header = "后台管理"
admin.site.index_title = "后台管理"

# 全站禁用批量删除功能
# admin.site.disable_action('delete_selected')


class PostAdmin(admin.ModelAdmin):
    def tags_list(self, post):  # 显示多对多字段
        """自定义列表字段"""
        tag_names = map(lambda x: x.name, post.tags.all())
        return ', '.join(tag_names)
    tags_list.short_description = "标签"
    tags_list.admin_order_field = 'created_time'   # 排序字段

    list_display = ['id', 'title', 'category', 'author', 'series', 'categorys', 'colored_status', 'comment_status', 'views', 'created_time', 'modified_time', 'tags_list']
    fieldsets = [
        ('文章内容', {'fields': ['title', 'body', 'excerpt', 'author']}),
        ('分类 & 标签', {'fields': ['category', 'tags']}),
        # ('状态', {'fields': [('status', 'categorys', 'series')]}),  # 显示到一行
        ('状态', {'classes': ('collapse',), 'fields': ['status', 'categorys', 'series', 'comment_status']}),
    ]
    list_filter = ['category', 'series', 'author__username', 'created_time']
    search_fields = ('title', 'excerpt', 'body')
    
    # list_editable 设置默认可编辑字段
    list_editable = ['series', 'categorys']
    
    # 分页，每页显示条数
    list_per_page = 10
    date_hierarchy = 'created_time'    # 详细时间分层筛选

    # 设置哪些字段可以点击进入编辑界面
    list_display_links = ('id', 'title')

    # Many to many 字段
    # filter_vertical = ('tags',)
    filter_horizontal = ('tags',)
    
    def get_readonly_fields(self, request, obj=None):
        """  重新定义此函数，限制普通用户所能修改的字段  """
        if request.user.is_superuser:
            self.readonly_fields = []
        return self.readonly_fields

    readonly_fields = ('title',)
    
    # 定义批量动作
    actions = ['make_published', 'make_drafted']
    
    def make_published(self, request, queryset):
        rows_updated = queryset.update(status='0')
        if rows_updated == 1:
            message_bit = "1 篇文章被"
        else:
            message_bit = "%s 篇文章被" % rows_updated
        self.message_user(request, "%s成功修改为发布状态" % message_bit)
    make_published.short_description = "发布"

    def make_drafted(self, request, queryset):
        rows_updated = queryset.update(status='1')
        if rows_updated == 1:
            message_bit = "1 篇文章被"
        else:
            message_bit = "%s 篇文章被" % rows_updated
        self.message_user(request, "%s成功修改为存稿状态" % message_bit)
    make_drafted.short_description = "存稿"
    
    # 非admin用户不能批量删除
    def get_actions(self, request):
        actions = super(PostAdmin, self).get_actions(request)
        if request.user.username.upper() != 'ADMIN':
            if 'delete_selected' in actions:
                del actions['delete_selected']
        return actions
    

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created_time']
    search_fields = ('name',)
    list_filter = ['created_time']
    # 分页，每页显示条数
    list_per_page = 15

    # 设置哪些字段可以点击进入编辑界面
    list_display_links = ('id', 'name')

    
class TagAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created_time']
    search_fields = ('name',)
    list_filter = ['created_time']
    # 分页，每页显示条数
    list_per_page = 15
    # 设置哪些字段可以点击进入编辑界面
    list_display_links = ('id', 'name')


class SeriesAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'created_time']
    search_fields = ('name',)
    list_filter = ['created_time']
    # 分页，每页显示条数
    list_per_page = 15
    # 设置哪些字段可以点击进入编辑界面
    list_display_links = ('id', 'name')
    

class LinkAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'url', 'description', 'created_time']
    search_fields = ('name', 'url', 'description')
    list_filter = ['created_time']
    # 分页，每页显示条数
    list_per_page = 15
    # 设置哪些字段可以点击进入编辑界面
    list_display_links = ('id', 'name')
    

class SettingAdmin(admin.ModelAdmin):
    list_display = ['id', 'body', 'pages', 'post_pic']
    search_fields = ('body',)
    # 分页，每页显示条数
    list_per_page = 15
    # 设置哪些字段可以点击进入编辑界面
    list_display_links = ('id', 'body')


class NoticeAdmin(admin.ModelAdmin):
    list_display = ['id', 'content', 'status', 'add_time']
    search_fields = ('content',)
    # 分页，每页显示条数
    list_per_page = 15
    # 设置哪些字段可以点击进入编辑界面
    list_display_links = ('id', 'content', 'status')


admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Series, SeriesAdmin)
admin.site.register(Link, LinkAdmin)
admin.site.register(Setting, SettingAdmin)
admin.site.register(Notice, NoticeAdmin)

