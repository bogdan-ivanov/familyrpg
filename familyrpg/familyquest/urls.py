from django.conf.urls import patterns, url

urlpatterns = patterns('',
	url(r'^photo_upload/$', 'familyquest.views.photo_upload', name='photo_upload'),
)