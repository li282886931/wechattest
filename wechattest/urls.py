from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'wechattest.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^itcastcpp/admin/', include(admin.site.urls)),
    url(r'^itcastcpp/wxbase/', include('wxbase.urls')),

)
