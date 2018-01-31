from django.conf.urls import url,include
from . import views

app_name="myForum"

urlpatterns=[
    url(r'^$', views.index, name='home'),
    url(r'^gettoken', views.gettoken, name='gettoken'),
]