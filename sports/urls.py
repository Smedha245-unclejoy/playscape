from django.conf.urls import url
from .views import SportView,SportFollowerView,SportsFollowedByUser

from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'follow/$', SportFollowerView.as_view(), name='follow_sport'),
    url(r'followedlist/(?P<user_id>\d+)/$',SportsFollowedByUser.as_view() , name='sports_followed'),
    url(r'^$', SportView.as_view(),name='create_sport')

]

urlpatterns = format_suffix_patterns(urlpatterns)
