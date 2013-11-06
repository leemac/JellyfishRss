from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:

from django.contrib import admin
admin.autodiscover()

from rss.views import IndexView
from rss.views import AboutView

urlpatterns = patterns('',
    # Examples:
    url(r'^$', IndexView.as_view(), name='index-view'),
    url(r'^login/', 'rss.views.login_user'),
    url(r'^logout/', 'rss.views.logout_user', name='logout-user'),
    url(r'^about/', AboutView.as_view(), name='about-view'),
    url('', include('django.contrib.auth.urls')),
    # url(r'^rss/', include('rss.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
) 
