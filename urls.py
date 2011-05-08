from django.conf.urls.defaults import patterns, include, url
from django.contrib.auth.views import login,logout

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'main.views.index'),
    url(r'^accounts/login/$', login , { 'template_name' : 'accounts/templates/login.html' } ),
    url(r'^accounts/logout/$', logout  ),
    url(r'^admin/', include(admin.site.urls)),
)
