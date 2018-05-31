from django.conf.urls import url
from . import views


nearby_users = views.NearbyUserList.as_view({
    'get': 'list',
    'post': 'create'
})

urlpatterns = [
    url(r'^$', views.UserCreate.as_view(), name='account-create'),
    url(r'(?P<username>[^/]+)/(?P<current_latitude>-?\d{2,3}.\d{5})/(?P<current_longitude>-?\d{2,3}.\d{5})/$', nearby_users, name='nearby_users'),
    url(r'/update',views.AuthInfoUpdateView.as_view(),name='account-update'),
]
