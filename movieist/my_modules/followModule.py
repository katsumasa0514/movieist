from ..models import Follow
from django.contrib import messages


def follow(request):
    if (request.method == 'POST'):
        if (request.user.id):
            if (request.POST["follow"] == request.user.id):
                pass

            elif (Follow.objects.filter(owner=request.user.id, following=request.POST["follow"])):
                Follow.objects.filter(owner=request.user.id,
                                      following=request.POST["follow"]).delete()
                Follow.objects.filter(
                    owner=request.POST["follow"], follower=request.user.id).delete()

            else:
                createFollowing = Follow.objects.filter(owner=request.user.id).create(
                    following=request.POST["follow"], owner_id=request.user.id)
                createFollowing.save()
                createFollower = Follow.objects.filter(owner=request.POST["follow"]).create(
                    follower=request.user.id, owner_id=request.POST["follow"])
                createFollower.save()
        else:
            messages.error(request, 'Followするにはログインが必要です。')
