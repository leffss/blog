from django.contrib import admin
from .models import Comment
# Register your models here.


admin.site.site_title = "后台管理"
admin.site.site_header = "后台管理"
admin.site.index_title = "后台管理"


class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'post', 'name', 'email', 'url', 'text', 'created_time']
    fieldsets = [
        ('评论内容', {'fields': ['name', 'email', 'url', 'text']}),
        ('所属文章', {'fields': ['post']}),
    ]
    search_fields = ('text', 'post__title') # post__title 外键
    # 分页，每页显示条数
    list_per_page = 15
    
    # 设置哪些字段可以点击进入编辑界面
    list_display_links = ['id', 'post', 'name', 'email']
    
    list_filter = ['post', 'name', 'created_time']
    
    
admin.site.register(Comment, CommentAdmin)

