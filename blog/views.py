from django.core.mail import send_mail
from django.db.models import Count, Q, F
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
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
                Q(categories__name__icontains=query) | Q(regions__name__icontains=query)
            ).distinct()

        context = {'queryset': queryset}
        template = '_includes/search.html'
        return render(request, template, context)


class IndexView(View):
    def get(self, request, *args, **kwargs):
        object_list = Post.published.prefetch_related('categories')
        region = Regions.objects.filter()

        context = {'posts': object_list, 'region': region}
        template = 'post/blog_post_listing.html'

        return render(request, template, context)

def post_detail(request, year, month, day, post):
    page_title = post.title
    region = Regions.objects.all()
    all_posts = Post.published.order_by('-publish')[:4]
    post = get_object_or_404(
        Post, slug=post, status='published', publish__year=year,
        publish__month=month, publish__day=day)

    posts = Post.published.all()
    paginator = Paginator(posts, 1)
    page = request.GET.get('page')
    try:
        pagination = paginator.page(page)
    except PageNotAnInteger:
        pagination = paginator.page(1)
    except EmptyPage:
        pagination = paginator.page(paginator.num_pages)


    # liste des articles les plus vues
    counter = Post.published.filter(title__gt=F('counter'))

    # Liste des articles similaires
    post_tags_ids = post.categories.values_list('id', flat=True)
    similar_posts = Post.published.defer("image").filter(
        categories__in=post_tags_ids).exclude(id=post.id).annotate(
        ).prefetch_related('categories').order_by('-publish')[:4]

    context = {
        'region': region, 'post': post, 'page_title': page_title, 'count': counter,
        'similar_posts': similar_posts, 'posts': all_posts, 'pagination': pagination
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


class ListTag(ListView):
    model = Categorie
    context_object_name = 'posts'
    template_name = 'post/blog_liste_categorie.html'
    paginate_by = 10

    def get_queryset(self):
        return Post.published.all().order_by('-publish')

    def get_context_data(self, **kwargs):
        context = super(ListTag, self).get_context_data(**kwargs)
        cat_listing = Categorie.objects.all()
        paginator = Paginator(cat_listing, self.paginate_by)
        page = self.request.GET.get('page')
        try:
            pagination = paginator.page(page)
        except PageNotAnInteger:
            pagination = paginator.page(1)
        except EmptyPage:
            pagination = paginator.page(paginator.num_pages)

        context['page_title'] = 'catégories'
        context['pagination'] = pagination

        return context


class ListByTag(ListView):
    "Liste des articles de même catégorie"
    model = Categorie
    context_object_name = 'posts'
    template_name = 'post/blog_liste_by_categorie.html'
    paginate_by = 10

    def get_queryset(self):
        self.cat = Categorie.objects.get(slug=self.kwargs['slug'])
        return Post.objects.filter(categories=self.cat).order_by('-publish')

    def get_context_data(self, **kwargs):
        context = super(ListByTag, self).get_context_data(**kwargs)
        cat_listing = Categorie.objects.all()
        paginator = Paginator(cat_listing, self.paginate_by)
        page = self.request.GET.get('page')
        try:
            pagination = paginator.page(page)
        except PageNotAnInteger:
            pagination = paginator.page(1)
        except EmptyPage:
            pagination = paginator.page(paginator.num_pages)

        context.update({'cat': self.cat})
        context['pagination'] = pagination

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
