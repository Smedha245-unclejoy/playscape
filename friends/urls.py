from django.conf.urls import url
from .views import RequestFriendship,AcceptFriendship

urlpatterns = [
       url(r'^create$',RequestFriendship.as_view(), name='friend-request'),
       url(r'^accept$',AcceptFriendship.as_view(), name='accept-request'),
]
