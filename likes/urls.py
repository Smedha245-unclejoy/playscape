from django.conf.urls import url
from .views import postpreference
from .views import createcomments

urlpatterns = [
       url(r'^(?P<postid>\d+)/preference/(?P<userpreference>\d+)/$',postpreference, name='postpreference'),
       url(r'^comments/$',createcomments, name='createcomments')
]
