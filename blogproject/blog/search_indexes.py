from haystack import indexes
from .models import Post


class PostIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    views = indexes.IntegerField(model_attr='views')

    def get_model(self):
        return Post

    def index_queryset(self, using=None):
        # return self.get_model().objects.all()
        return self.get_model().objects.filter(status='0')
