from django.urls import path
from . import views
from .feeds import LatestPostsFeed


urlpatterns = [
    path("", views.project_list, name="project_list"),
    path("projects/<slug:category_slug>/", views.project_list, name='project_list_by_category'),
    path("projects/<int:pk>/<slug:slug>/", views.project_detail, name="project_detail"),

    path('blog/', views.post_list, name='post_list'),
    path('blog/<int:year>/<int:month>/<int:day>/<slug:post>/', views.post_detail, name='post_detail'),
    path('blog/<int:post_id>/share/', views.post_share, name='post_share'),
    path('blog/tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),
    path('blog/feed/', LatestPostsFeed(), name='post_feed'),
    path('blog/search/', views.post_search, name='post_search'),
]