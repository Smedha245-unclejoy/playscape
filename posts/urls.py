from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from .views import Upload,AllPosts,PostDetail,PostFeed
from rest_framework.urlpatterns import format_suffix_patterns



#post_list = Upload.as_view({
#    'get': 'list',
#    'post': 'create'
#})
urlpatterns = [
    url(r'^$', Upload.as_view(), name='post-create'),
    url(r'(?P<post_id>\d+)/$', PostDetail.as_view(),name='post_detail'),
    url(r'getall/(?P<user_id>\d+)/$', AllPosts.as_view(), name='all_posts'),
    url(r'postfeed/$', PostFeed.as_view(), name='post-feed')

]

urlpatterns = format_suffix_patterns(urlpatterns)
