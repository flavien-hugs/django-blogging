from django import template
from django.db.models import Count
from ..models import Post, Categorie
from django.utils.safestring import mark_safe

import markdown

register = template.Library()

@register.simple_tag(takes_context=True)
def pageviews(context):
    try:
        request = context['request']
        count = Post.objects.get(slug=request.path)
        return count.counter
    except Post.DoesNotExist:
        return 0


@register.simple_tag
def pageviews_url(path):
    try:
        count = Post.objects.get(slug=path)
        return count.counter
    except Post.DoesNotExist:
        return 0

@register.inclusion_tag('post/blog_latest_post.html')
def show_latest_posts(count=5):
    latest_posts = Post.published.filter(created__isnull=False).order_by('-publish')[:count]
    context = { 'latest_posts': latest_posts }
    return context

@register.inclusion_tag('post/categories/politique.html')
def show_politique_posts(count=1):
    politique =  Post.published.filter(created__isnull=False).order_by('-publish')[:count]
    context = { 'politique': politique }
    return context

@register.inclusion_tag('post/categories/economie.html')
def show_economie_posts(count=1):
    economie =  Post.published.filter(created__isnull=False).order_by('-publish')[:count]
    context = { 'economie': economie }
    return context

@register.inclusion_tag('post/categories/education.html')
def show_education_posts(count=1):
    education =  Post.published.filter(created__isnull=False).order_by('-publish')[:count]
    context = { 'education': education }
    return context

@register.inclusion_tag('post/blog_categorie_liste.html')
def show_allcategorie():
    allcategorie = Categorie.objects.order_by('name')
    return {'allcategorie': allcategorie}

@register.inclusion_tag('post/blog_archive_by_year.html')
def archive_by_year():
    year_list = Post.objects.dates('publish','year', order='ASC')
    return {'year_list': year_list}

@register.inclusion_tag('post/blog_archive_by_month.html')
def archive_by_month():
    month_list = Post.objects.dates('publish','month', order='DESC')
    return {'month_list': month_list}

@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))

@register.simple_tag
def total_posts():
    return Post.published.count()
