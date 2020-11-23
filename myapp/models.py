from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.contrib.auth.signals import user_logged_in, user_logged_out
import datetime


# Create your models here.
class Stock(models.Model):
    favorite = models.ManyToManyField(User, related_name='fav_set')
    portfolio_list = models.ManyToManyField(User, related_name='port_set', through='Portfolio')
    current_user = models.ForeignKey(User, related_name='owner', null=True, on_delete=models.SET_NULL)

    symbol = models.CharField(max_length=12, primary_key=True)
    name = models.CharField(max_length=64)
    change_over_time = models.FloatField(null=True)
    top_rank = models.IntegerField(null=True)
    price = models.FloatField(null=True)
    change = models.FloatField(null=True)
    change_percent = models.FloatField(null=True)
    market_cap = models.FloatField(null=True)
    primary_exchange = models.CharField(null=True, max_length=32)

# class stockManager(models.Manager):
#
#     def all_with_related_users(self):
#         qs = self.get_queryset()
#         qs = qs.select_related(
#             'portfolio_list')
#         qs = qs.prefetch_related(
#             'writers', 'actors')
#         return qs

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth = models.CharField(max_length=100, default='',blank=True)
    city = models.CharField(max_length=100, default='',blank=True)
    job = models.CharField(max_length=300, default='',blank=True)
    bio = models.CharField(max_length=300, default='',blank=True)
    website = models.URLField(default='', blank=True)
    image = models.ImageField(
        blank=True, upload_to='profile_pics', default='profile.png')

    def __str__(self):
        return self.user.username


class Activity(models.Model):
    user = models.ForeignKey(
        User, related_name='log_user', null=True, on_delete=models.SET_NULL)
    type = models.CharField(max_length=100, default='')
    # date =  models.DateField(default=datetime.date.today())
    time = models.DateTimeField(default=datetime.datetime.now())

class Choices(models.Model):
    mChoices = (
        ('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'),
        ('10', '10'), ('11', '11'), ('12', '12'))
    yChoices = (('1', '20'), ('2', '22'), ('3', '23'), ('4', '24'), ('5', '25'))

    month = models.CharField(max_length=300, choices= mChoices)
    year = models.CharField(max_length=300, choices=yChoices)

def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = Profile.objects.create(user=kwargs['instance'])


class Portfolio(models.Model):
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_price = models.FloatField(null=True)
    date = models.DateTimeField(default=datetime.datetime.now())
    shares = models.IntegerField(null=True)

    class Meta:
        unique_together = [['user','stock']]


def log_user_login(sender, user, **kwargs):
    print("logged in: ", user.email)
    new_activity = Activity.objects.create(
        user=user,
        type='Login',
        time=datetime.datetime.now())


def log_user_logout(sender, user, **kwargs):
    print("logged out: ", user.email)
    new_activity = Activity.objects.create(
        user=user,
        type='Logout',
        time=datetime.datetime.now())


user_logged_in.connect(log_user_login, sender=User)
user_logged_out.connect(log_user_logout, sender=User)
post_save.connect(create_profile, sender=User)
