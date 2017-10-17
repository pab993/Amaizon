from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.login_page, name='login_page'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^index/$', views.index, name='index'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
    url(r'^profile/$', views.profile, name='profile')
]
