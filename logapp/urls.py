from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^user/vote/$', views.vote, name='vote'),
]
