from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^create$', views.item_page, name='itemPage'),
    url(r'^add_item$', views.add_item, name='addItem'),
    url(r'^logout$', views.logout, name='logOut'),
    url(r'^wish_items/(?P<id>\d+)$', views.item_specific, name='itemSpecific'),
    url(r'^wishlist_add/(?P<id>\d+)$', views.wishlist_add, name='wishListAdd'),
    url(r'^item_delete/(?P<id>\d+)$', views.delete_item, name='itemDelete'),
    url(r'^wishlist_remove/(?P<id>\d+)$', views.wishlist_remove, name='wishlistRemove'),

]
