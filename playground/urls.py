from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from .views import PlaygroundView


urlpatterns = [
    url(r'playground$', PlaygroundView.as_view(),name='create-playground'),

]

urlpatterns = format_suffix_patterns(urlpatterns)
