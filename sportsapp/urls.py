from django.conf.urls import url
from . import views


nearby_users = views.NearbyUserList.as_view({
    'get': 'list',
    'post': 'create'
})

urlpatterns = [
    url(r'^$', views.UserCreate.as_view(), name='account-create'),
    url(r'(?P<username>[^/]+)/(?P<current_latitude>-?\d{2,3}.\d{5})/(?P<current_longitude>-?\d{2,3}.\d{5})/$', nearby_users, name='nearby_users'),
    url(r'update', views.AuthInfoUpdateView.as_view(), name='account-update'),
    url(r'profile', views.SelfCreateProfile.as_view(), name='profile-create'),
    url(r'get', views.GetUser.as_view(), name='get-user'),
    url(r'all', views.GetAllUsers.as_view(),name='all-users'),
    url(r'get/user/(?P<user_id>\d+)$',views.GetUserThroughId.as_view(), name='getuser_through_id'),
]
