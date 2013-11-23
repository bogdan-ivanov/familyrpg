from tastypie.resources import ModelResource
from tastypie.authorization import Authorization
from .models import FamilyMember, Family, Chore, Badge, ChoreVote, Reward
from tastypie import fields


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
		excludes = ['email', 'password', 'is_active', 'is_staff', 'is_superuser']
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
	class Meta:
		queryset = Reward.objects.all()
		resource_name = 'reward'
		authorization = Authorization()
