from datetime import datetime

import pytest
from django.test import TestCase

from navoica_enroll.users.forms import UserCreationForm, UserRegistrationCourseForm
from navoica_enroll.users.models import User
from navoica_enroll.users.tests.factories import UserFactory

pytestmark = pytest.mark.django_db


class TestUserCreationForm:
    def test_clean_username(self):
        # A user with proto_user params does not exist yet.
        proto_user = UserFactory.build()

        form = UserCreationForm(
            {
                "username": proto_user.username,
                "password1": proto_user._password,
                "password2": proto_user._password,
            }
        )

        assert form.is_valid()
        assert form.clean_username() == proto_user.username

        # Creating a user.
        form.save()

        # The user with proto_user params already exists,
        # hence cannot be created.
        form = UserCreationForm(
            {
                "username": proto_user.username,
                "password1": proto_user._password,
                "password2": proto_user._password,
            }
        )

        assert not form.is_valid()
        assert len(form.errors) == 1
        assert "username" in form.errors


class TestUserRegisterForm(TestCase):
    fixtures = ['users.json', ]


    def setUp(self):
        self.user = User.objects.get(id=1)
        self.valid_form = {
            'first_name': self.user.first_name,
            'last_name': self.user.last_name,
            'gender': 'M',
            'pesel': '53022858449',
            'citizenship': 'Polish',
            'age': 30,
            'education': 3,
            'street': "Test",
            'street_no': "Test",
            'street_building_no': "Test",
            'postal_code': "00-001",
            'city': 'Szczecin',
            'voivodeship': 'west_pomerania',
            'county': 'szczecin',
            'country': 'PL',
            'commune': 'Test',
            'start_project_date': datetime.now(),
            'end_project_date': datetime.now(),
            'start_support_date': datetime.now(),
            'phone': 432423,
            'email': 'longemaillongemaillongemaillongemail@longemaillongemaillongemaillongemail.pl',
            'status': 'employed',
            'status_info': 'other',
            'profession': 'Farmer',
            'work_name': "Test",
            'origin': "y",
            'homeless': "n",
            'disabled_person': "n",
            'social_disadvantage': "n",
            'statement1': True,
            'statement2': True
        }

    def test_register_pl(self):

        form = UserRegistrationCourseForm(
            self.valid_form
        )

        assert form.is_valid()

        obj = form.save(commit=False)

        assert not obj.pk

        obj.user = self.user
        obj.save()

        assert obj.pk

        assert obj.email == 'longemaillongemaillongemaillongemail@longemaillongemaillongemaillongemail.pl'


    def test_postalcode(self):

        tmp_form = self.valid_form
        tmp_form['postal_code'] = "55-080" #polish
        form = UserRegistrationCourseForm(
            self.valid_form
        )
        assert form.is_valid()

        tmp_form = self.valid_form
        tmp_form['postal_code'] = "99501" #US postal code
        form = UserRegistrationCourseForm(
            self.valid_form
        )
        assert form.is_valid()

        tmp_form = self.valid_form
        tmp_form['postal_code'] = "asd234ss"  # invalid postal code
        form = UserRegistrationCourseForm(
            self.valid_form
        )
        assert not form.is_valid()

