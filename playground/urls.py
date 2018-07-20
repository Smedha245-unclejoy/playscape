from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from .views import PlaygroundView,AllPlaygroundList


urlpatterns = [
    url(r'create$', PlaygroundView.as_view(),name='create-playground'),
    url(r'all$', AllPlaygroundList.as_view(),name='all-playgrounds'),

]

urlpatterns = format_suffix_patterns(urlpatterns)
