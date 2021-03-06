from django.db import models
from django.contrib.auth.models import User
from model_utils.models import TimeStampedModel
import datetime
from django.core.urlresolvers import reverse


class ChoreOverdue(Exception):
    pass

class NotAuthorizedMember(Exception):
    pass


class Family(models.Model):
    name = models.CharField('Family Name', max_length=200)
    def chores(self):
        return [ {
                    'id': c.pk ,
                    'text': c.text ,
                    'resource_uri': reverse('api_dispatch_list', kwargs={'resource_name': 'chore', 'api_name': 'v1'}) + str(c.pk) + "/",
                    'xp_reward': c.xp_reward,
                    'deadline': c.deadline,
                    'voting': c.state == ChoreStates.VOTING,
                } \
                for c in Chore.objects.all() if c.initiator in self.members.all() \
                        and c.state in [ChoreStates.INITIALIZED, ChoreStates.VOTING]]

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Families'


class FamilyMember(User):
    family = models.ForeignKey(Family, related_name='members')
    xp = models.IntegerField(default=0)

    def complete_chore(self, chore):

        if datetime.datetime.now() > chore.deadline:
            raise ChoreOverdue
        if self.pk not in chore.allowed_members:
            raise NotAuthorizedMember

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
    initiator = models.ForeignKey(FamilyMember)
    text = models.TextField('Description')
    deadline = models.DateTimeField('Due Time')
    xp_reward = models.IntegerField('XP Rewarded')
    state = models.IntegerField('Chore State', choices = ChoreStates.ALL, default=ChoreStates.INITIALIZED)
    allowed_members = models.ManyToManyField(FamilyMember, related_name="available_chores")
    achiever = models.ForeignKey(FamilyMember, related_name="achieved_chores", null=True, blank=True)

    def approve(self):
        if self.state != ChoreStates.VOTING:
            return {'error': 'Chore not in voting stage'}
        if self.achiever:
            self.achiever.xp += self.xp_reward
            self.achiever.save()
        self.state = ChoreStates.COMPLETED
        self.save()

        return {'state': 'completed'}

    def resolve(self, user):
        self.achiever = user
        self.state = ChoreStates.VOTING
        self.save()
        return {'state': 'voting'}

    def __unicode__(self):
        return self.text[:100] + " by " + unicode(self.initiator)


class ChoreVote(TimeStampedModel):
    voter = models.ForeignKey(FamilyMember, related_name="voter")
    chore = models.ForeignKey(Chore, related_name="chore")

    def __unicode__(self):
        return unicode(self.voter) + " voted for " + unicode(self.chore)


class RewardTypes:
    WATCH_TV = 0
    PLAY_GAMES = 1
    PLAY_FOOTBALL = 2

    ALL = (
        (WATCH_TV, 'Watch TV'),
        (PLAY_GAMES, 'Play Games'),
        (PLAY_FOOTBALL, 'Play Football')
    )


class Reward(TimeStampedModel):
    member = models.ForeignKey(FamilyMember, related_name='rewards')
    duration_seconds = models.IntegerField('Duration')
    reward_type = models.IntegerField(choices=RewardTypes.ALL, default=RewardTypes.WATCH_TV)
    consumed = models.BooleanField(default=False)
    xp_cost = models.IntegerField(default=100)



    @property
    def name(self):
        try:
            return RewardTypes.ALL[self.reward_type][1]
        except:
            return 'Fun Activity'

    def consume(self):
        if self.consumed:
            return {'error': 'reward already consumed'}
        if self.member.xp < self.xp_cost:
            return {'error': 'not enough XP!'}
        self.consumed = True
        self.save()
        self.member.xp -= self.xp_cost
        self.member.save()
        return {'state': 'consumed'}

