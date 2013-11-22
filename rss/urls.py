from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'rss.views.home', name='index-view'),
    url(r'^redirect-login/', 'rss.views.login_redirect', name='login-redirect-view'),
    url(r'^login/', 'rss.views.login_user', name='login-user'),
    url(r'^logout/', 'rss.views.logout_user', name='logout-user'),
    # url('', include('django.contrib.auth.urls')),
    # url(r'^rss/', include('rss.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
) 
