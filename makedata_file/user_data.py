from django.contrib.auth.models import User
from random import shuffle, seed
from faker.providers.person.en import Provider


name = list(set(Provider.name))
email = list(set(Provider.email))

seed(4321)
shuffle(name)
shuffle(email)

user, created = User.objects.get_or_create(name=name, email=email)
if created:
    user.set_password('nawa0514')
    user.save()

print(name[0:1000])


def add_user(request):
    fake = Faker('ja_JP')
    fake.random.seed(4321)

    name = set()
    while len(name) < 1000:
        name.add(fake.name())
        print(name)

    user, created = User.objects.get_or_create(username=fake_name, email=fake_email)
    if created:
        user.set_password('nawa0514')
        user.save()
    return user, created
