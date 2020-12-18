from django.db import models

# Create your models here.


class Search(models.Model):
    genres = models.CharField(max_length=20)
    image = models.URLField(max_length=200)
    title = models.CharField(max_length=100)
    userPic = models.ImageField(upload_to='documents/', default='defo')
    userName = models.CharField(max_length=50)
    good = models.IntegerField(default=0)
    bad = models.IntegerField(default=0)
    commentTitle = models.CharField(max_length=40)
    comment = models.TextField()
