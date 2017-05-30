from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^reviews$', views.reviews),
    url(r'^add_review$', views.add_review),
    url(r'^review/(?P<id>\d+)$', views.add_book_review),
    url(r'^add$', views.add),
    url(r'^books/(?P<id>\d+)$', views.book_info),
    url(r'^delete/(?P<id>\d+)$', views.delete),
    url(r'^users/(?P<id>\d+)$', views.users),
]
