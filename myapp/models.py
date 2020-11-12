from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.contrib.auth.signals import user_logged_in, user_logged_out
import datetime


# Create your models here.
class Stock(models.Model):
    favorite = models.ManyToManyField(User)
    current_user = models.ForeignKey(
        User, related_name='owner', null=True, on_delete=models.SET_NULL)

    @classmethod
    def make_favorite(cls, user, stock):

        stock.current_user = user
        stock.favorite.add(user)
        # stock, created = cls.objects.update_or_create(
        # 	current_user = user
        # )
        # stock.favorite.add(user)
        stock.save()

    @classmethod
    def unfavorite(cls, user, stock):
        # stock.current_user = user
        # Stock.objects.filter(pk=user.pk).update(current_user='')
        stock.favorite.remove(user)
        stock.save()

    symbol = models.CharField(max_length=12, primary_key=True)
    name = models.CharField(max_length=64)
    change_over_time = models.FloatField(null=True)
    top_rank = models.IntegerField(null=True)
    price = models.FloatField(null=True)
    change = models.FloatField(null=True)
    change_percent = models.FloatField(null=True)
    market_cap = models.FloatField(null=True)
    primary_exchange = models.CharField(null=True, max_length=32)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth = models.CharField(max_length=100, default='')
    city = models.CharField(max_length=100, default='')
    job = models.CharField(max_length=300, default='')
    bio = models.CharField(max_length=300, default='')
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


def create_profile(sender, **kwargs):
    if kwargs['created']:
        user_profile = Profile.objects.create(user=kwargs['instance'])


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
