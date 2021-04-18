from ..models import Review, Goodbad


def goodbad(request):
    if 'good' in request.POST:
        review_id = Review.objects.get(id=request.POST["id"])
        goodData, created = Goodbad.objects.get_or_create(
            owner=review_id, good=request.user.id)
        if created:
            review_id.countgood += 1
            review_id.save()

    if 'bad' in request.POST:
        review_id = Review.objects.get(id=request.POST["id"])
        badData, created = Goodbad.objects.get_or_create(
            owner=review_id, bad=request.user.id)
        if created:
            review_id.countbad += 1
            review_id.save()
