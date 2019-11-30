from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords

from .models import Post, Categorie

class LatestPostsFeed(Feed):
    """docstring for LatestPostsFeed"""
    title = u'My blog'
    link = '/blog/'
    description = u'New posts of my blog.'
    title_template=('feeds/feed_title.html')
    description_template=('feeds/feed_desc.html')

    def items(self):
        return Post.published.order_by('-publish')[:10]

    def item_title(self, item):
        return item.title

    def item_link(self, item):
        return item.get_absolute_url()

    def item_description(self, item):
        return item.body

    def item_description(self, item):
        return truncatewords(item.body, 30)

    def item_pubdate(self, item):
        return item.publish


class LatestPostsByTag(Feed):
    def get_object(self, request, monslug):
        return get_object_or_404(Categorie, slug=slug)

    def title(self, obj):
        return u"blogging - Catégorie %s" % (obj.name,)

    def link(self, obj):
        return obj.get_absolute_url()

    description = u"Derniers articles"
    title_template=('feeds/feed_title.html')
    description_template=('feeds/feed_desc.html')

    def items(self, obj):
        return Post.objects.filter(categories__name=obj).order_by('-publish')[:10]

    def item_title(self, obj):
        return obj.title

    def item_link(self, obj):
        return obj.get_absolute_url()

    def item_description(self, obj):
        return obj.body

    def item_pubdate(self, obj):
        return obj.publish
