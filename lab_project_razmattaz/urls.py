"""lab_project_razmattaz URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, include
from django.contrib import admin
from forum import views



urlpatterns = [
    url(r'^$',views.home,name='index'),
    url(r'^home/', views.index, name ='index_home'),
    url(r'^forum/', include('forum.urls', namespace='forum')),
    url(r'^microsoft/',include('microsoft_auth.urls',namespace='microsoft')),
    url(r'post/(?P<id>\d+)/',views.post_detail,name='post_detail'),
    url(r'post/new/$',views.post_new,name="post_new"),
    url(r'post/delete/(?P<id>\d+)/',views.post_delete,name="post_delete"),
    url(r'comment/new/(?P<id>\d+)/',views.comment_new,name="comment_new"),
    url(r'comment/delete/(?P<id>\d+)/',views.comment_delete,name="comment_delete"),
    url(r'logout/',views.logout,name="logout"),
    url(r'^admin/', admin.site.urls),
]
