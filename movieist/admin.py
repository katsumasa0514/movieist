from django.contrib import admin
from .models import Review, Profile, Follow, Goodbad

admin.site.register(Review)
admin.site.register(Profile)
admin.site.register(Follow)
admin.site.register(Goodbad)
