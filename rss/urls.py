from django.conf.urls import patterns, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'rss.views.home', name='index-view'),
    url(r'^redirect-login/', 'rss.views.login_redirect', name='login-redirect-view'),
    url(r'^login/', 'rss.views.login_user', name='login-user'),
    url(r'^logout/', 'rss.views.logout_user', name='logout-user'),
    url(r'^api/get_subscription_items', 'rss.views.get_subscription_items', name='get-subscription-items'),
    url(r'^api/get_folders', 'rss.views.get_folders', name='get-folders'),
    url(r'^api/add_subscription', 'rss.views.add_subscription', name='get-subscriptions'),
    url(r'^api/mark_subscription_read', 'rss.views.mark_subscription_read', name='mark-subscription-read'),
    url(r'^api/change_subscription_color', 'rss.views.change_subscription_color', name='change-subscription-color'),
) 
