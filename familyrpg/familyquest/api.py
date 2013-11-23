from tastypie.resources import ModelResource
from tastypie.authorization import Authorization
from .models import FamilyMember, Family, Chore, Badge
from tastypie import fields


class FamilyResource(ModelResource):
	class Meta:
		queryset = Family.objects.all()
		resource_name = 'family'
		authorization= Authorization()


class FamilyMemberResource(ModelResource):
	family = fields.ForeignKey(FamilyResource, 'family')
	class Meta:
		queryset = FamilyMember.objects.all()
		resource_name = 'family_member'
		excludes = ['email', 'password', 'is_active', 'is_staff', 'is_superuser']
		authorization= Authorization()


class ChoreResource(ModelResource):
	class Meta:
		queryset = Chore.objects.all()
		resource_name = 'chore'
		authorization= Authorization()


class BadgeResource(ModelResource):
	class Meta:
		queryset = Badge.objects.all()
		resource_name = 'badge'
		authorization= Authorization()
