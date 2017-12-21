import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'logpro.settings'

import django
django.setup()

from faker import Faker
import random
from logapp.models import StudentUser, Candidate
from django.contrib.auth.models import User

fake = Faker()

#Create fake user
def create_fake_user():
    new_user = False
    while not new_user:
        username = fake.name()
        first_name = username.split()[0]
        last_name = username.split()[1]
        password = 'adminadmin'
        email = fake.simple_profile(sex=None)['mail']
        user_tup = User.objects.get_or_create(username = username, first_name=first_name,
                last_name=last_name, email=email, password=password)
        new_user = user_tup[1]
    user = user_tup[0]
    user.save()
    user.set_password(password)
    user.save()
    return user

def create_fake_student():
    user = create_fake_user()
    year_groups = ['2020', '2021', '2022', '2023']

    unique_id = False
    while not unique_id:
        year = random.choice(year_groups)
        pin = str(random.randint(0,9999))
        id = int(pin + year)
        query = StudentUser.objects.filter(student_id = id)
        if len(query) == 0:
            unique_id = True
    student = StudentUser.objects.create(user = user, student_id = id)
    student.save()
    return student

if __name__ == '__main__':
    num_of_users = 10
    print('Preparing to create {0} fake users'.format(num_of_users))
    for i in range(num_of_users):
        create_fake_student()
        print('{0} users created.'.format(i+1))
