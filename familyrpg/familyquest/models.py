from django.db import models
from django.contrib.auth.models import User
from model_utils.models import TimeStampedModel
import datetime


class ChoreOverdue(Exception):
    pass


class Family(models.Model):
    name = models.CharField('Family Name', max_length=200)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Families'


class FamilyMember(User):
    family = models.ForeignKey(Family)
    xp = models.IntegerField(default=0)

    def complete_chore(self, chore):
        if datetime.datetime.now() > chore.deadline:
            raise ChoreOverdue
        self.xp += chore.xp_reward
        chore.achiever = self
        chore.state = ChoreStates.COMPLETED
        chore.save();

    class Meta:
        verbose_name_plural = 'Family members'
        verbose_name = 'Family member'


class Badges:
    SUPREME_CLEANER = 1
    FAMOUS_DOGWALKER = 2
    HOMEWORK_TYCOON = 3

    ALL = (
        (SUPREME_CLEANER, 'Supreme Cleaner'),
        (FAMOUS_DOGWALKER, 'Famous Dogwalker'),
        (HOMEWORK_TYCOON, 'Homework Tycoon'),
    )


class Badge(TimeStampedModel):
    owner = models.ForeignKey(FamilyMember)
    badge_type = models.IntegerField(choices=Badges.ALL, default=Badges.SUPREME_CLEANER)

    def __unicode__(self):
        return unicode(self.owner) + " - " + self.badge_type



class ChoreStates:
    INITIALIZED = 1
    VOTING = 2
    COMPLETED = 3

    ALL = (
        (INITIALIZED, 'INITIALIZED'),
        (VOTING, 'VOTING'),
        (COMPLETED, 'COMPLETED'),
    )


class Chore(TimeStampedModel):
    initiator = models.ForeignKey(FamilyMember, related_name="initiator")
    text = models.TextField('Description')
    deadline = models.DateTimeField('Due Time')
    xp_reward = models.IntegerField('XP Rewarded')
    state = models.IntegerField('Chore State', choices = ChoreStates.ALL, default=ChoreStates.INITIALIZED)
    allowed_members = models.ManyToManyField(FamilyMember, related_name="allowed_members")
    achiever = models.ForeignKey(FamilyMember, related_name="achiever", null=True, blank=True)

    def __unicode__(self):
        return self.text[:100] + " by " + unicode(self.initiator)


