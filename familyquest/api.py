from tastypie.resources import ModelResource
from tastypie.authorization import Authorization
from .models import FamilyMember, Family, Chore, Badge, ChoreVote, Reward
from tastypie import fields
from django.conf.urls import url
from tastypie.utils import trailing_slash
from tastypie.authentication import ApiKeyAuthentication



class FamilyResource(ModelResource):
    members = fields.ToManyField('familyquest.api.FamilyMemberResource', attribute='members', readonly=True)
    available_chores = fields.ListField(attribute='chores', readonly=True)
    class Meta:
        queryset = Family.objects.all()
        resource_name = 'family'
        authorization= Authorization()

        authentication = ApiKeyAuthentication()


class FamilyMemberResource(ModelResource):
    family = fields.ForeignKey(FamilyResource, 'family')
    rewards = fields.ToManyField('familyquest.api.RewardResource', attribute='rewards', readonly=True)
    chores = fields.ToManyField('familyquest.api.ChoreResource', attribute='available_chores', readonly=True)
    class Meta:
        queryset = FamilyMember.objects.all()
        resource_name = 'family_member'
        excludes = ['email', 'password', 'is_active', 'is_staff', 'is_superuser', 'last_name']
        authorization= Authorization()

        authentication = ApiKeyAuthentication()


class ChoreResource(ModelResource):
    #votes = fields.ToManyField('ChoreVoteResource', 'votes', null=True, blank=True)
    initiator = fields.ForeignKey('familyquest.api.FamilyMemberResource', 'initiator')
    allowed_members = fields.ToManyField('familyquest.api.FamilyMemberResource', 'allowed_members')
    class Meta:
        queryset = Chore.objects.all()
        resource_name = 'chore'
        authorization= Authorization()

        authentication = ApiKeyAuthentication()

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/resolve%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('resolve'), name="api_chore_resolve"),

            url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/approve%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('approve'), name="api_chore_approve"),
        ]

    def resolve(self, request, **kwargs):
         """ proxy for the chore.resolve method """

         self.method_check(request, allowed=['get'])

         chore = self.cached_obj_get(
             bundle=self.build_bundle(request=request),
             **self.remove_api_resource_names(kwargs))

         user = FamilyMember.objects.get(username=request.GET['username'])

         return self.create_response(request, chore.resolve(user))

    def approve(self, request, **kwargs):
         """ proxy for the chore.approve method """

         self.method_check(request, allowed=['get'])

         chore = self.cached_obj_get(
             bundle=self.build_bundle(request=request),
             **self.remove_api_resource_names(kwargs))

         return self.create_response(request, chore.approve())


class BadgeResource(ModelResource):
    class Meta:
        queryset = Badge.objects.all()
        resource_name = 'badge'
        authorization= Authorization()

        authentication = ApiKeyAuthentication()


class ChoreVoteResource(ModelResource):
    chore = fields.ForeignKey(ChoreResource, 'chore')
    voter = fields.ForeignKey(FamilyMemberResource, 'voter')
    class Meta:
        queryset = Badge.objects.all()
        resource_name = 'chore_vote'
        authorization = Authorization()

        authentication = ApiKeyAuthentication()

class RewardResource(ModelResource):
    name = fields.CharField(attribute='name', readonly=True, blank=True, null=True)
    class Meta:
        queryset = Reward.objects.all()
        resource_name = 'reward'
        authorization = Authorization()

        authentication = ApiKeyAuthentication()

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/consume%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('consume'), name="api_reward_consume"),
        ]

    def consume(self, request, **kwargs):
         """ proxy for the reward.consume method """

         self.method_check(request, allowed=['get'])

         reward = self.cached_obj_get(
             bundle=self.build_bundle(request=request),
             **self.remove_api_resource_names(kwargs))

         return self.create_response(request, reward.consume())



from tastypie.models import create_api_key
from django.db import models
models.signals.post_save.connect(create_api_key, sender=FamilyMember)
