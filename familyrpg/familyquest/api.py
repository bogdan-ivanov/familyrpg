from tastypie.resources import ModelResource
from tastypie.authorization import Authorization
from .models import FamilyMember, Family, Chore, Badge, ChoreVote, Reward
from tastypie import fields
from django.conf.urls import url
from tastypie.utils import trailing_slash



class FamilyResource(ModelResource):
    members = fields.ToManyField('familyquest.api.FamilyMemberResource', attribute='members', readonly=True)
    available_chores = fields.ListField(attribute='chores', readonly=True)
    class Meta:
        queryset = Family.objects.all()
        resource_name = 'family'
        authorization= Authorization()


class FamilyMemberResource(ModelResource):
    family = fields.ForeignKey(FamilyResource, 'family')
    rewards = fields.ToManyField('familyquest.api.RewardResource', attribute='rewards', readonly=True)
    chores = fields.ToManyField('familyquest.api.ChoreResource', attribute='available_chores', readonly=True)
    class Meta:
        queryset = FamilyMember.objects.all()
        resource_name = 'family_member'
        excludes = ['email', 'password', 'is_active', 'is_staff', 'is_superuser', 'last_name']
        authorization= Authorization()


class ChoreResource(ModelResource):
    votes = fields.ToManyField('ChoreVoteResource', 'votes', null=True, blank=True)
    class Meta:
        queryset = Chore.objects.all()
        resource_name = 'chore'
        authorization= Authorization()


class BadgeResource(ModelResource):
    class Meta:
        queryset = Badge.objects.all()
        resource_name = 'badge'
        authorization= Authorization()


class ChoreVoteResource(ModelResource):
    chore = fields.ForeignKey(ChoreResource, 'chore')
    voter = fields.ForeignKey(FamilyMemberResource, 'voter')
    class Meta:
        queryset = Badge.objects.all()
        resource_name = 'chore_vote'
        authorization = Authorization()

class RewardResource(ModelResource):
    name = fields.CharField(attribute='name', readonly=True, blank=True, null=True)
    class Meta:
        queryset = Reward.objects.all()
        resource_name = 'reward'
        authorization = Authorization()

    def prepend_urls(self):
        return [
            url(r"^(?P<resource_name>%s)/(?P<pk>\w[\w/-]*)/consume%s$" %
                (self._meta.resource_name, trailing_slash()),
                self.wrap_view('consume'), name="api_reward_consume"),
        ]

    def consume(self, request, **kwargs):
         """ proxy for the reward.consume method """

         # you can do a method check to avoid bad requests
         self.method_check(request, allowed=['get'])

         # using the primary key defined in the url, obtain the game
         print kwargs
         reward = self.cached_obj_get(
             bundle=self.build_bundle(request=request),
             **self.remove_api_resource_names(kwargs))

         # Return what the method output, tastypie will handle the serialization
         return self.create_response(request, reward.consume())
