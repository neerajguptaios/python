from django.conf.urls import url
from .views import BlogPostRudView, BlogPostAPIView, BlogPostListAPIView, BlogPostListCreateAPIView

urlpatterns = [
    url(r'^$', BlogPostListCreateAPIView.as_view(),name='post-list-with-create'),
    url(r'^list/$', BlogPostListAPIView.as_view(),name='post-list-without-create'),
    url(r'^create/$', BlogPostAPIView.as_view(),name='post-create'),
    url(r'^(?P<pk>\d+)/$', BlogPostRudView.as_view(),name='post-rud')
]
