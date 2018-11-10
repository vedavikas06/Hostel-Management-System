from django.contrib import admin
from django.urls import path
from . import views as guest_view
from django.conf.urls import include, url

app_name = 'guest'
urlpatterns = [
    path(r'', guest_view.home, name='home'),
    path(r'select/<int:res_id>/', guest_view.select, name='select'),
    # url(r'profile/^$', guest_view.profile, name='profile'),
    path(r'edit/<int:res_id>/', guest_view.edit, name='edit'),
    path(r'confirm/<int:res_id>/', guest_view.confirm, name='confirm'),
    path(r'cancel/<int:res_id>/', guest_view.cancel, name='cancel'),
]