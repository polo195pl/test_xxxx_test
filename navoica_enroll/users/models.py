from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import CharField
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from localflavor.pl.pl_voivodeships import VOIVODESHIP_CHOICES

from navoica_enroll.users.administrative_units import ADMINISTRATIVE_UNIT_CHOICES_PL, NATIONALITIES_CHOICES
from navoica_enroll.variables import COUNTRIES_ENROLL


class User(AbstractUser):
    name = CharField(_("Name of User"), blank=True, null=True, max_length=255)

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"username": self.username})


class UserRegistrationCourse(models.Model):
    first_name = models.CharField(_("First Name"), max_length=100)
    last_name = models.CharField(_("Last name"), max_length=100)
    citizenship = models.CharField(_("Citizenship"), max_length=100, choices=NATIONALITIES_CHOICES)
    gender = models.CharField(_("Gender"), choices=[
        ('', _('Select...')),
        ('M', _('Male')),
        ('F', _('Female')),
    ], max_length=1)
    pesel = models.CharField(_("PESEL"), null=True, blank=True, max_length=11)
    age = models.SmallIntegerField(_("Age"))
    education = models.CharField(_("Education"), max_length=1,
                                 choices=[
                                     ('', _('Select...')),
                                     ('1', _('Pre-primary')),
                                     ('2', _('Primary')),
                                     ('3', _('Secondary')),
                                     ('4', _('High school')),
                                     ('5', _('Higher'))
                                 ]
                                 )
    street = models.CharField(_("Street"), max_length=300,
                              help_text=_("Enter the address postal address."))
    street_no = models.CharField(_("Street no"), max_length=10)
    street_building_no = models.CharField(_("Building no"), max_length=10, null=True, blank=True)
    postal_code = models.CharField(_("Postal code"), max_length=6)
    city = models.CharField(_("City"), max_length=30)
    voivodeship = models.CharField(_("Voivodeship"), default="", max_length=30, null=True,
                                   blank=True,
                                   choices=sorted(VOIVODESHIP_CHOICES,
                                                  key=lambda x: x[1]))
    county = models.CharField(_("County"), default="", max_length=30, null=True, blank=True,
                              choices=sorted(ADMINISTRATIVE_UNIT_CHOICES_PL,
                                             key=lambda x: x[1]))
    commune = models.CharField(_("Commune"), max_length=30, null=True,
                               blank=True)

    country = models.CharField(_("Country"), max_length=30, choices=COUNTRIES_ENROLL, default="ZZ")

    phone = models.CharField(_("Phone"), max_length=30)
    email = models.CharField(_("E-mail"), max_length=254)
    start_project_date = models.DateField(_("Start project date"),
                                          default=timezone.now)
    end_project_date = models.DateField(_("End project date"),
                                        default=timezone.now)
    start_support_date = models.DateField(_("Start support date"),
                                          default=timezone.now)

    STATUSES = (
        ('', _('Select...')),
        ('employed', _('Employed')),
        ('registered', _('Registered unemployed')),
        ('unregistered', _('Unregistered unemployed')),
        ('looking', _('Unemployed, not looking for work')),
    )

    status = models.CharField(_("What is your current status on the labor market?"), max_length=1000,
                              choices=STATUSES
                              )

    status_info = models.CharField(_("Status additional information"), max_length=1000, null=True, blank=True)

    PROFESSIONS = [
        "",
        _("Vocational teacher"),
        _("General education teacher"),
        _("Kindergarten teacher"),
        _("Employee in higher education institution"),
        _("Labor market institution employee"),
        _("Health care worker"),
        _("Farmer"),
        _("Key employee in social assistance and integration institution"),
        _("Employee in family and foster care support institution"),
        _("Employee in social economy support center"),
        _("Employee in psychological and pedagogical counseling center"),
        _("Practical vocational instructor"),
        _("other"),
    ]

    profession = models.CharField(_("Profession"), max_length=1000, null=True, blank=True,
                                  choices=[(t, t) for t in
                                           PROFESSIONS])

    work_name = models.CharField(_("Company's name"), max_length=1000, null=True, blank=True, )

    origin = models.CharField(
        _("Do you belong to a national or ethnic minority, are you a migrant, a person of foreign origin?"),
        max_length=1, default="", choices=[
            ('y', _("Yes")),
            ('n', _("No")),
            ('r', _("Prefer not to tell"))

        ])
    homeless = models.CharField(_("Are you homeless or excluded from housing?"), max_length=1, default="", choices=[
        ('y', _("Yes")),
        ('n', _("No")),
        ('r', _("Prefer not to tell"))

    ])
    disabled_person = models.CharField(_("Are you a person with a disability?"), max_length=1, default="",
                                       choices=[
                                           ('y', _("Yes")),
                                           ('n', _("No")),
                                           ('r', _("Prefer not to tell"))

                                       ])
    social_disadvantage = models.CharField(_("Are you a socially disadvantaged person?"),
                                           max_length=1, default="", choices=[
            ('y', _("Yes")),
            ('n', _("No")),
            ('r', _("Prefer not to tell"))
        ])

    course_id = models.CharField(_("Course ID"), max_length=1000)
    language_code = models.CharField(_("Form language"), max_length=1000)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    def __str__(self):
        return "{}: {} {}".format(self.course_id, self.user.first_name,
                                  self.user.last_name)

    @property
    def navoica_id(self):
        try:
            return self.user.socialaccount_set.filter(provider='edx')[0].extra_data['id']
        except:
            return ""

    @property
    def navoica_email(self):
        try:
            return self.user.socialaccount_set.filter(provider='edx')[0].extra_data['email']
        except:
            return ""

    @property
    def navoica_username(self):
        try:
            return self.user.socialaccount_set.filter(provider='edx')[0].extra_data['username']
        except:
            return ""

    class Meta:
        verbose_name = _("Registration for course")
        verbose_name_plural = _("Registrations for course")
