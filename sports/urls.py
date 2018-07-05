from .views import SportView,SportFollowerView,SportsFollowedByUser,AllSports,SportUpdate
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'follow/$', SportFollowerView.as_view(), name='follow_sport'),
    url(r'followedlist/$',SportsFollowedByUser.as_view() , name='sports_followed'),
    url(r'^$', SportView.as_view(),name='create_sport'),
    url(r'all/$', AllSports.as_view(),name='allsports'),
    url(r'update/$',SportUpdate.as_view(),name='sport-update')

]
urlpatterns = format_suffix_patterns(urlpatterns)
