from django.conf.urls import patterns, include, url
from familyquest.api import FamilyMemberResource, BadgeResource, ChoreResource, \
		FamilyResource, ChoreVoteResource, RewardResource
from tastypie.api import Api
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
admin.autodiscover()

v1_api = Api(api_name='v1')
v1_api.register(FamilyMemberResource())
v1_api.register(BadgeResource())
v1_api.register(ChoreResource())
v1_api.register(FamilyResource())
v1_api.register(ChoreVoteResource())
v1_api.register(RewardResource())


urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'familyrpg.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include(v1_api.urls)),
    url(r'^', include('familyquest.urls'))
) #+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
