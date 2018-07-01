from django.conf.urls import url
from .views import SportView
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    url(r'^$', SportView.as_view(),name='create_sport')

]

urlpatterns = format_suffix_patterns(urlpatterns)
