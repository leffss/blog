from django.db import models


class Comment(models.Model):
    name = models.CharField(max_length=100, verbose_name='评论人')
    email = models.EmailField(max_length=255, verbose_name='电子邮箱')
    url = models.URLField(blank=True, verbose_name='地址URL', null=True)
    text = models.TextField(verbose_name='内容')
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='添加时间')
    post = models.ForeignKey('blog.Post', verbose_name='文章', on_delete=models.CASCADE)
    # parent = models.ForeignKey('self', verbose_name='父评论', related_name='%(class)s_child_comments', blank=True, null=True)
    # rep_to = models.ForeignKey('self', verbose_name='回复', related_name='%(class)s_rep_comments', blank=True, null=True)

    def __str__(self):
        return self.text[:20]
    
    class Meta:
        verbose_name = '评论'
        verbose_name_plural = '评论'
        ordering = ['created_time']

