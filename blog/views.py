from django.db.models import Count, Q, F
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views.generic import (
    View, ListView, DetailView, DayArchiveView,
    MonthArchiveView, YearArchiveView, DateDetailView )

from .forms import EmailPostForm
from .models import PostView, Post, Regions, Categorie

# Create your views here.

# fonction de recherche interne au blog
class SearchView(View):
    """docstring for SearchView"""
    def get(self, request, *args, **kwargs):
        queryset = Post.objects.all()
        query = request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) | Q(body__icontains=query) |
                Q(categories__name__icontains=query)
            ).distinct()

        context = {'queryset': queryset}
        template = '_includes/search.html'
        return render(request, template, context)


class IndexView(View):
    def get(self, request, *args, **kwargs):
        categorie = Categorie.objects.all()
        object_list = Post.published.filter(categories__in=categorie)
        region = Regions.objects.filter()

        context = {'posts': object_list, 'region': region, 'tag': categorie}
        template = 'post/blog_post_listing.html'

        return render(request, template, context)

def post_detail(request, year, month, day, post):
    page_title = post.title
    region = Regions.objects.all()
    post = get_object_or_404(
        Post, slug=post, status='published', publish__year=year,
        publish__month=month, publish__day=day)

    # Liste des articles similaires
    post_tags_ids = post.categories.values_list('id', flat=True)
    similar_posts = Post.published.filter(
        categories__in=post_tags_ids).exclude(id=post.id).annotate(
        same_tags=Count('categories', distinct=True)
        ).prefetch_related('categories').order_by('-same_tags', '-publish')[:4]

    context = {
        'region': region, 'post': post, 'page_title': page_title,
        'similar_posts': similar_posts
    }

    template = 'post/blog_post_detail.html'

    return render(request, template, context)

def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            post_url = request.build_absolute_uri(post.get_absolute_url())
            subject = '{} ({}) recommends you reading "{}"'.format(cd['name'], cd['email'], post.title)
            message = 'Read "{}" at {}\n\n{}\'s comments: {}'.format(post.title, post_url, cd['name'], cd['comments'])
            send_mail(subject, message, 'flavienhgs@gmail.com', [cd['to']])
            sent = True
    else:
        form = EmailPostForm()

    context = {'post': post, 'form': form, 'sent': sent}
    template = 'post/share.html'
    return render(request, template, context)


class ListByTag(ListView):
    "Liste des articles de même catégorie"

    context_object_name = 'posts'
    template_name = 'post/blog_categorie_liste.html'

    def get_queryset(self):
        self.cat = Categorie.objects.get(slug=self.kwargs['slug'])
        return Post.objects.filter(categories=self.cat).order_by('-publish')

    def get_context_data(self, **kwargs):
        context = super(ListByTag, self).get_context_data(**kwargs)
        context.update({'cat': self.cat})
        return context


class DayView(DayArchiveView):
    month_format = '%m'
    date_field = 'publish'
    queryset = Post.objects.all()


class MonthView(MonthArchiveView):
    month_format = '%m'
    year_format = '%Y'
    date_field = 'publish'
    queryset = Post.objects.all()


class YearView(YearArchiveView):
    date_field = 'publish'
    queryset = Post.objects.all()
