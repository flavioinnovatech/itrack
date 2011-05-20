from django.shortcuts import render_to_response
from django.conf.urls.defaults import *
from django.contrib.auth.views import login,logout,logout_then_login,password_reset
from django.conf import settings
from itrack.system.forms import UserCompleteForm, SettingsForm, SystemForm, SystemWizard


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from dajaxice.core import dajaxice_autodiscover
dajaxice_autodiscover()

urlpatterns = patterns('',
url(r'^$', 'main.views.index'),
url(r'^accounts/login/$', 'accounts.views.login' ),
url(r'^accounts/logout/$', logout_then_login),
url(r'^accounts/$', 'accounts.views.index'),

url(r'^admin/', include(admin.site.urls)),
url(r'^media/(.*)$', 'django.views.static.serve', {'document_root' : settings.MEDIA_ROOT}),
url(r'^accounts/profile/$', 'main.views.index'),
url(r'^themes/$', 'themes.views.index'),

#url(r'^grid/$', 'grid.views.index'),

url(r'^system/$','system.views.index'),
url(r'^system/create/$','system.views.create'),
url(r'^system/edit/(\d+)/$','system.views.edit'),
url(r'^system/delete/(\d+)/$','system.views.delete'),
url(r'^system/finish/$','system.views.finish'),
url(r'^system/edit/finish/$','system.views.editfinish'),
url(r'^system/delete/finish/$','system.views.deletefinish'),
url(r'^equipment/$','equipments.views.index'),
url(r'^equipment/permissions/(\d+)/$','equipments.views.permissions'),
url(r'^equipment/associations/(\d+)/$','equipments.views.associations'),
url(r'^equipment/finish/$','equipments.views.finish'),

url(r'^rastreamento/veicular/$', 'rastreamento.views.index'),
url(r'^rastreamento/portatil/$', 'rastreamento.views.index'),

url(r'^accounts/create/$', 'accounts.views.create_user'),
url(r'^accounts/edit/(\d+)/$','accounts.views.edit'),
url(r'^accounts/delete/(\d+)/$','accounts.views.delete'),
url(r'^accounts/ajax/delete/$','accounts.ajax.delete'),

url(r'^accounts/password_reset/$', 'django.contrib.auth.views.password_reset', {'template_name':'accounts/templates/password_reset_form.html', 'email_template_name':'accounts/templates/password_reset_email.html'}),
url(r'^password_reset/done/$', 'django.contrib.auth.views.password_reset_done', {'template_name':'userpanel/password_reset_done.html'}),
url(r'^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'django.contrib.auth.views.password_reset_confirm', {'template_name':'userpanel/password_reset_confirm.html'}),
url(r'^reset/done/$', 'django.contrib.auth.views.password_reset_complete', {'template_name':'userpanel/password_reset_complete.html'}),

(r'^%s/' % settings.DAJAXICE_MEDIA_PREFIX, include('dajaxice.urls')),


)
