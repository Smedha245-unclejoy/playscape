from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from .views import PlaygroundView,AllPlaygroundList,UpdatePlayground


urlpatterns = [
    url(r'create$', PlaygroundView.as_view(),name='create-playground'),
    url(r'all$', AllPlaygroundList.as_view(),name='all-playgrounds'),
    url(r'update$', UpdatePlayground.as_view(),name='update-playgrounds'),

]

urlpatterns = format_suffix_patterns(urlpatterns)
