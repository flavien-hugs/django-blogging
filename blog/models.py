from django.db import models
from django.urls import reverse
from django.utils import dateformat, timezone
from django.contrib.auth import get_user_model
from django.core.files.storage import default_storage

import markdown

User = get_user_model()

class PostView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Regions(models.Model):
    """docstring for Tag"""
    name = models.CharField('Regions', max_length=50)

    class Meta:
        verbose_name_plural = 'regions'
        ordering = ('name',)

    def __str__(self):
        return self.name

class Categorie(models.Model):
    """docstring for Tag"""
    name = models.CharField('Categorie name', max_length=50)
    slug = models.SlugField('Référence', help_text='Automatiquement formé à partir du titre.')

    class Meta:
        verbose_name_plural = 'catégories'
        ordering = ('name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:list_by_tag', args=[self.slug])


class PublishedManager(models.Manager):
    """docstring for PublishedManager"""
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )

    categories = models.ManyToManyField(Categorie, verbose_name="Catégorie(s)")
    regions = models.ManyToManyField(Regions, verbose_name="Régions")
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField("Titre de l'article", max_length=100)
    slug = models.SlugField('lien url', max_length=100, help_text='Automatiquement formé à partir du titre.', unique_for_date='publish')
    image = models.ImageField('Image associée', upload_to='images/', blank=True, null=True)
    body = models.TextField('Contenu HTML', help_text='Utilisez la syntaxe HTML.', blank=True, null=True)
    counter = models.PositiveIntegerField(default=0)
    publish = models.DateTimeField('Date de publication', default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField('Status', max_length=10, choices=STATUS_CHOICES, default='draft')

    objects = models.Manager()
    published = PublishedManager()

    def __str__(self):
        return "%s (%s)" % (
            self.name, ", ".join(categorie.name for categorie in self.categories.all()),)

    class Meta:
        ordering = ('-publish',)
        get_latest_by = 'publish'
        verbose_name_plural = "Posts"

    def get_absolute_url(self):
        good_date = timezone.localtime(self.publish)
        return reverse(
            'blog:post_detail',
            args=[self.slug, self.publish.year, self.publish.month, self.publish.day]
        )

    def save(self):
        """Vérifications avant l'enregistrement"""
        try:
            old_img = Post.objects.get(pk=self.id)
            path = old_img.image.path
            if old_img.image.path != self.image.path:
                default_storage.delete(path)
            elif self.remove_image:
                self.image = None
                default_storage.delete(path)
        except:
            pass
        self.remove_image = False
        super(Post, self).save()

    # liste des articles les plus vues
    @property
    def view_count(self):
        return PostView.objects.filter(post=self).count()
