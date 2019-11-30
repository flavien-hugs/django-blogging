__author__ = 'Flavien-hugs <contact@unsta.ci>'
__version__= '0.0.1'
__copyright__ = '© 2019 unsta'

from django.contrib import admin
from .models import Regions, Categorie, Post


# Register your models here.

@admin.register(Regions)
class RegionsAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Categorie)
class CategorieAdmin(admin.ModelAdmin):
    list_display = ['name']
    prepopulated_fields = {
        'slug': ('name',)
    }

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """
    @admin.register(Post)
        Admin View for Post
    """
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')
    raw_id_fields = ('author',)
    list_display = ('author', 'title', 'slug', 'publish', 'status')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'body')

    class Media:
        js = (
            'js/tiny_mce/tiny_mce.js',
            'js/admin_pages.js'
        )
        css = {"all": ("css/admin.css",)}
