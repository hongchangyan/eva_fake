from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
                       url(r'eva_fake/', include('eva_fake.api.urls'))
                       )
