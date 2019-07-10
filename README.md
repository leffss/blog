# blog
基于 python 3.7 + django 2.2.3 + Metro-UI-CSS 4.3 等一大堆前端插件实现的 blog 系统，响应式并且自适应手机客户端，推荐 1920*1080 及以上分辨率访问。


# 主要功能
- Django 自带的admin后台管理系统，推荐使用 simpleui：https://github.com/newpanjing/simpleui
- 发布文章使用markdown，支持代码高亮
- 文章分类、标签、归档、系列、浏览量统计等
- 文章评论系统，验证码回复，支持关闭文章评论
- 滚动公告系统
- 全文搜索功能
- RSS 博客订阅功能及 Sitemap 网站地图
- 友情链接
- 文章详情缓存系统


# 安装
```
# 安装相关库
pip install -r requirements.txt

# 初始化数据库
python manage.py makemigrations
python manage.py migrate

# 创建 admin 后台账号
python manage.py createsuperuser

# 运行
python manage.py runserver
```
- 默认使用 `sqlites`，如果需要使用其他数据库，比如 `mysql`，方法自行查阅 `django` 官方文档
- django 自带的 server 只能做开发测试用。生产部署一般2种方式：Nginx+uwsgi 或者 nginx+gunicorn，具体方法自行上网搜索

访问首页：http://127.0.0.1:8000
访问后台：http://127.0.0.1:8000/admin


# 效果
### 首页
![效果](https://github.com/leffss/blog/blob/master/uploads/1.png?raw=true)
![效果](https://github.com/leffss/blog/blob/master/uploads/2.png?raw=true)

### 文章详情
![效果](https://github.com/leffss/blog/blob/master/uploads/3.png?raw=true)
![效果](https://github.com/leffss/blog/blob/master/uploads/4.png?raw=true)

### 评论
![效果](https://github.com/leffss/blog/blob/master/uploads/5.png?raw=true)

### 搜索
![效果](https://github.com/leffss/blog/blob/master/uploads/6.png?raw=true)

### 手机浏览效果
![效果](https://github.com/leffss/blog/blob/master/uploads/7.png?raw=true)
![效果](https://github.com/leffss/blog/blob/master/uploads/8.png?raw=true)

### 后台管理
![效果](https://github.com/leffss/blog/blob/master/uploads/9.png?raw=true)


# TODO
- [ ] 评论回复功能
- [ ] 首页文章轮播


