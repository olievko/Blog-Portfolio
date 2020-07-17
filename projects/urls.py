from django.urls import path

from .views.projects import project_list, project_detail, message_sent
from .views.posts import post_list, post_detail, post_share
# from .views.posts import PostsSearch
from .feeds import LatestPostsFeed

urlpatterns = [
    path("", project_list, name="project_list"),
    path("projects/<slug:category_slug>/", project_list, name='project_list_by_category'),
    path("projects/<int:pk>/<slug:slug>/", project_detail, name="project_detail"),
    path("success", message_sent, name="message_sent"),

    path('blog/', post_list, name='post_list'),
    path('blog/<int:year>/<int:month>/<int:day>/<slug:post>/', post_detail, name='post_detail'),
    path('blog/<int:post_id>/share/', post_share, name='post_share'),
    path('blog/tag/<slug:tag_slug>/', post_list, name='post_list_by_tag'),
    path('blog/feed/', LatestPostsFeed(), name='post_feed'),
    path('blog/search/', post_list, name='posts_search'),
    # path('blog/search/', PostsSearch.as_view(), name='posts_search'),
]
