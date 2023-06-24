from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import secrets
from PIL import Image

# Create your models here.

# Model Class Profile
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default='0')
    picture = models.ImageField('image')
    bio = models.TextField()

    def __str__(self):
        return self.user.username

    @classmethod
    def update_profile(cls, id, user, bio, picture):
        cls.objects.filter(id=id).update(user=user, bio=bio, picture=picture)

    def save_profile(self):
        self.save()

    def delete_profile(self):
        self.delete()

# Model Class Polls
class Poll(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    pub_date = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(default=True)

    def user_can_vote(self, user):
        """ 
        Return False if user already voted
        """
        user_votes = user.vote_set.all()
        qs = user_votes.filter(poll=self)
        if qs.exists():
            return False
        return True

    @property
    def get_vote_count(self):
        return self.vote_set.count()


    def get_result_dict(self):
        res = []
        for choice in self.choice_set.all():
            d = {}
            alert_class = ['primary', 'secondary', 'success',
                           'danger', 'dark', 'warning', 'info']

            d['alert_class'] = secrets.choice(alert_class)
            d['text'] = choice.choice_text
            d['num_votes'] = choice.get_vote_count
            if not self.get_vote_count:
                d['percentage'] = 0
            else:
                d['percentage'] = (choice.get_vote_count /
                                   self.get_vote_count)*100

            res.append(d)
        return res
    def __str__(self):
        return self.description

# Model Class Choice
class Choice(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.poll.description[:25]} - {self.choice_text[:25]}"

    @property
    def get_vote_count(self):
        return self.vote_set.count()

# Model Class Vote
class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.poll.description[:15]} - {self.choice.choice_text[:15]} - {self.user.username}'


