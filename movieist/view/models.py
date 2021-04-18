from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    userPic = models.ImageField(
        upload_to='documents/', default='documents/default_image1.png')
    userComment = models.TextField(default='コメントがありません')


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        Follow.objects.create(owner=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Review(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='review_owner')
    commentTitle = models.CharField(max_length=100)
    comment = models.TextField()
    movie_id = models.IntegerField()
    star = models.DecimalField(default=0, max_digits=2, decimal_places=1)
    datetime = models.DateTimeField(default=timezone.now)
    countgood = models.IntegerField(default=0)
    countbad = models.IntegerField(default=0)
    genre = models.CharField(max_length=20)
    title = models.CharField(max_length=150)
    image_path = models.CharField(max_length=100)


@receiver(post_save, sender=Review)
def create(sender, instance, created, **kwargs):
    if created:
        Goodbad.objects.create(owner=instance)


class Goodbad(models.Model):
    owner = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='goodbad_owner')
    good = models.IntegerField(null=True)
    bad = models.IntegerField(null=True)


class Follow(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follow_owner')
    following = models.IntegerField(null=True)
    follower = models.IntegerField(null=True)
    countfollowing = models.IntegerField(default=0)
    countfollower = models.IntegerField(default=0)
