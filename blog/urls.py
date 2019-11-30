from django.urls import path

from .feeds import LatestPostsFeed
from blog.views import SearchView, IndexView, ListByTag, post_detail, post_share, DayView, MonthView, YearView

app_name = 'blog'

urlpatterns = [
    path('', IndexView.as_view(), name='post_listing'),
    path('search/', SearchView.as_view(), name='search'),
    path('categorie/<slug:slug>/', ListByTag.as_view(), name='list_by_tag'),
    path('<int:year>/<int:month>/<int:day>/<slug:post>/', post_detail, name='post_detail'),
    path('<int:year>/<int:month>/<int:day>/', DayView.as_view(), name="day_archive"),
    path('<int:year>/<int:month>/', MonthView.as_view(), name="month_archive"),
    path('<int:year>/', YearView.as_view(), name="year_archive"),
    path('<int:post_id>/share/', post_share, name='post_share'),
    path('feed/', LatestPostsFeed(), name='post_feed'),
]
