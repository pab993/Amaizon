from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.login_page, name='login_page'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login_user/$', views.login_user, name='login_user'),
    url(r'^index/$', views.index, name='index'),
    url(r'^logout_user/$', views.logout_user, name='logout_user'),
    url(r'^profile/$', views.profile, name='profile'),
    url(r'^product/(?P<product_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^controlPanel/$', views.control, name='control'),
    url(r'^editProduct/$', views.newgame, name='editProduct'),
    url(r'^editProduct/(?P<product_id>[0-9]+)/$', views.newgame, name='editProduct'),
    url(r'^deleteProduct/(?P<product_id>[0-9]+)/$', views.deletegame, name='deleteProduct'),
]
