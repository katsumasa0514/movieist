from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

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


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class Review(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='review_owner')
    commentTitle = models.CharField(max_length=40)
    comment = models.TextField()
    movie_id = models.IntegerField()
    good = models.IntegerField(default=0)
    bad = models.IntegerField(default=0)
    star = models.DecimalField(default=0, max_digits=2, decimal_places=1)


class Follow(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follow_owner')
    following = models.IntegerField(default=0)
    follower = models.IntegerField(default=0)
