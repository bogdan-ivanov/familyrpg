from django.contrib import admin
from .models import Badge, Chore, Family, FamilyMember, ChoreVote, Reward
from tastypie.models import ApiAccess

class BadgeAdmin(admin.ModelAdmin):
    pass

class ChoreAdmin(admin.ModelAdmin):
    pass

class FamilyAdmin(admin.ModelAdmin):
    pass

class FamilyMemberAdmin(admin.ModelAdmin):
    pass

class ChoreVoteAdmin(admin.ModelAdmin):
    pass

class RewardAdmin(admin.ModelAdmin):
    pass

class ApiAccessAdmin(admin.ModelAdmin):
    pass

admin.site.register(Badge, BadgeAdmin)
admin.site.register(Chore, ChoreAdmin)
admin.site.register(Family, FamilyAdmin)
admin.site.register(FamilyMember, FamilyMemberAdmin)
admin.site.register(ChoreVote, ChoreVoteAdmin)
admin.site.register(Reward, RewardAdmin)
admin.site.register(ApiAccess, ApiAccessAdmin)