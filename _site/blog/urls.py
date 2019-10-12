from django.urls import path
from . import views
from .feeds import LatestPostsFeed

app_name = 'blog'
urlpatterns = [
    path('', views.post_listing, name='post_listing'),
    path('tag/<slug:tag_slug>/', views.post_listing, name='post_listing_by_tag'),
    # path('', views.PostListView.as_view(), name='post_listing'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail'),
    path('<int:post_id>/share/', views.post_share, name='post_share'),
    path('search/', views.post_search, name='post_search'),
    path('feed/', LatestPostsFeed(), name='post_feed'),
]
