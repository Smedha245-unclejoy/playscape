from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from .views import CreateEventView,UpdateParticipatorStatus


urlpatterns = [
    url(r'create$', CreateEventView.as_view(),name='create-event'),
    url(r'partcipator_status_update$',UpdateParticipatorStatus.as_view(),name='update-status') ,

]

urlpatterns = format_suffix_patterns(urlpatterns)
