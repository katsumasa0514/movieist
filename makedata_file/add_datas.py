def add_user(request):
    fake = Faker('ja_JP')
    fake.random.seed(4321)

    names = set()
    emails = set()
    while len(names) < 1000:

        len(emails)
        names.add(fake.name())
        emails.add(fake.email())

    for (name, email) in zip(names, emails):
        user, created = User.objects.get_or_create(username=name, email=email)
        if created:
            user.set_password('nawa0514')
            user.save()
    return user, created


def add_csv(request):
    if 'csv' in request.FILES:
        form_data = TextIOWrapper(request.FILES['csv'].file, encoding='utf-8')
        csv_file = csv.reader(form_data)
        for line in csv_file:
            movie_info = api.get_movie(line[0])
            image = api.get_movie_images(line[0])
            genres = movie_info['genres'][0]['name']
            number = random.randrange(1, 1000)
            numbers = User.objects.get(id=number)
            review = Review()
            review.owner = numbers
            review.movie_id = line[0]
            review.title = line[1]
            review.commentTitle = line[2]
            review.comment = line[3]
            review.star = line[4]
            review.genre = genres
            try:
                review.image_path = f"{api.img_base_url_}{image['posters'][0]['file_path']}"
            except IndexError:
                review.image_path = '/media/documents/noimage.jpg'
            review.save()

        return render(request, 'movieist/add_csv.html')

    else:
        return render(request, 'movieist/add_csv.html')


def add_follow(request):
    for i in range(1, 1000):
        number_1 = random.randrange(2, 10)
        for er in range(1, number_1):
            user = User.objects.get(id=i)
            follow = Follow()
            follow.owner = user
            number_2 = random.randrange(1, 1000)
            follow.follower = number_2
            follow.save()

        number_3 = random.randrange(2, 10)
        for er in range(1, number_3):
            user = User.objects.get(id=i)
            follow = Follow()
            follow.owner = user
            number_4 = random.randrange(1, 1000)
            follow.following = number_4
            follow.save()


def add_goodbad(request):
    for i in range(1, 778):
        number_1 = random.randrange(2, 10)
        for g in range(1, number_1):
            review_id = Review.objects.get(id=i)
            goodbad = Goodbad()
            goodbad.owner = review_id
            number_2 = random.randrange(1, 1000)
            goodbad.good = number_2
            goodbad.save()
            review_id.countgood += 1
            review_id.save()
        number_3 = random.randrange(2, 10)
        for b in range(1, number_3):
            review_id = Review.objects.get(id=i)
            goodbad = Goodbad()
            goodbad.owner = review_id
            number_4 = random.randrange(1, 1000)
            goodbad.bad = number_4
            goodbad.save()
            review_id.countbad += 1
            review_id.save()
