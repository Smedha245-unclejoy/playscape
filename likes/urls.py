from django.conf.urls import url
from .views import createcomments,postpreference,GetPreference

urlpatterns = [
       url(r'^(?P<postid>\d+)/preference/(?P<userpreference>\d+)/$',postpreference, name='postpreference'),
       url(r'^comments/$',createcomments, name='createcomments'),
       url(r'get/user/(?P<user_id>\d+)/post/(?P<post_id>\d+)$',GetPreference.as_view(),name='get-preference'),
       url(r'^comments/all/(?P<post_id>\d+)$',CommentsForPost.as_view(),name='comments-on-post'),
]
