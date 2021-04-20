from ..models import Review, Goodbad
from django.contrib import messages


def goodbad(request):
    if 'good' in request.POST:
        if (request.user.id):
            review_id = Review.objects.get(id=request.POST["id"])
            goodData, created = Goodbad.objects.get_or_create(
                owner=review_id, good=request.user.id)
            if created:
                review_id.countgood += 1
                review_id.save()
        else:
            messages.error(request, 'Goodするにはログインが必要です。')

    if 'bad' in request.POST:
        if (request.user.id):
            review_id = Review.objects.get(id=request.POST["id"])
            badData, created = Goodbad.objects.get_or_create(
                owner=review_id, bad=request.user.id)
            if created:
                review_id.countbad += 1
                review_id.save()
        else:
            messages.error(request, 'Badするにはログインが必要です。')
