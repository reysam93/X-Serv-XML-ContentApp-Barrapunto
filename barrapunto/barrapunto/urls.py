from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',

    url(r'^admin/', include(admin.site.urls)),
    url(r'^update', 'contentApp.views.updateNews'),
    url(r'^(.*)$', 'contentApp.views.processRequest')
)
