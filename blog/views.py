from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post, Comment
from django.db.models import Count
from .forms import EmailPostForm, CommentForm, SearchForm
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, TrigramSimilarity
from django.core.mail import send_mail


from taggit.models import Tag


# Create your views here.

class PostListView(ListView):
    queryset = Post.published.all()
    context_object_name = 'posts'
    paginate_by = 3
    template_name = 'post/listing.html'


def post_listing(request, tag_slug=None):
    object_list = Post.published.all()
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = object_list.filter(tags__in=[tag])

    paginator = Paginator(object_list, 10)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    context = {'posts': posts, 'page': page, 'tag': tag}
    template = 'post/listing.html'

    return render(request, template, context)


def post_detail(request, year, month, day, post):
    post = get_object_or_404(
        Post, slug=post, status='published', publish__year=year,
        publish__month=month, publish__day=day
    )

    # Liste des articles similaires
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.published.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags', '-publish')[:4]

    # Liste active des commentaires pour un post
    comments = post.comments.filter(active=True)
    new_comment = None

    if request.method == 'POST':
        # on affiche un commentaire
        form_comment = CommentForm(data=request.POST)
        if form_comment.is_valid():
            # creation d'un objet commentaire et ne pas l'enregistrer dans BD
            new_comment = form_comment.save(commit=False)
            # On affecte le message courrant au commentaire
            new_comment.post = post
            # sauvegarde dans la BD
            new_comment.save()
    else:
        form_comment = CommentForm()

    context = {
        'post': post, 'comments': comments,
        'new_comment': new_comment, 'form_comment': form_comment,
        'similar_posts': similar_posts
    }
    template = 'post/detail.html'

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


def post_search(request):
    form = SearchForm()
    query = None
    results = []
    if 'query' in  request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            results = Post.objects.annotate(
                similarity=TrigramSimilarity('title', query),
            ).filter(similarity__gt=0.3).order_by('similarity')


    context = { 'form': form, 'query': query, 'results': results }
    template = 'post/search.html'

    return render(request, template, context)