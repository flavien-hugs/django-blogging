from django.db.models import F
from blog.models import Post

class PageViewsMiddleware:
    """docstring for PageViewsMiddleware"""
    def precess_request(self, request, *args, **kwargs):
        count, post_created = Post.objects.get_or_create(slug=request.path)
        count.counter = F('counter') + 1
        count.save()

        return None
