import json

import requests
import six
from allauth.socialaccount import providers
from allauth.socialaccount.models import SocialToken
from allauth.utils import get_request_param
from csv_export.views import CSVExportView
from dateutil import parser
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import FieldDoesNotExist
from django.core.serializers.json import DjangoJSONEncoder
from django.http import Http404, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.utils.translation import ugettext_lazy as _
from django.views import View
from django.views.generic import DetailView, RedirectView, UpdateView
from django.views.generic.edit import FormView

from .forms import UserRegistrationCourseEnglishForm, UserRegistrationCourseForm
from ..providers.edx.provider import EdxProvider
from ..variables import STATUSES_OPTIONS

User = get_user_model()


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    slug_field = "username"
    slug_url_kwarg = "username"


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ["name"]

    def get_success_url(self):
        return reverse("users:detail",
                       kwargs={"username": self.request.user.username})

    def get_object(self):
        return User.objects.get(username=self.request.user.username)

    def form_valid(self, form):
        messages.add_message(
            self.request, messages.INFO, _("Infos successfully updated")
        )
        return super().form_valid(form)


user_update_view = UserUpdateView.as_view()


class UserRedirectView(LoginRequiredMixin, RedirectView):
    permanent = False

    def get_redirect_url(self):
        return reverse("users:detail",
                       kwargs={"username": self.request.user.username})


user_redirect_view = UserRedirectView.as_view()


class CustomLoginView(View):
    def get(self, request, *args, **kwargs):

        try:
            provider = next(
                provider for provider in providers.registry.get_list() if type(provider) == EdxProvider
            )

            param_next = get_request_param(request, "next")
            query = {'next': param_next}
            url = provider.get_login_url(request, **query)
            return redirect(url)


        except StopIteration:
            return HttpResponse('Provider is not configured. Contact Admin.')


class UserRegistrationCourseViewBase(FormView):
    template_name = 'users/form_registration.html'
    success_url = '/thanks/'
    token = None
    course_info = None

    def get_form_class(self):
        if self.request.LANGUAGE_CODE == 'pl':
            return UserRegistrationCourseForm
        return UserRegistrationCourseEnglishForm

    def get_initial(self):
        initial = super().get_initial()
        if self.request.user.is_authenticated:
            initial['email'] = self.request.user.email
            initial['first_name'] = self.request.user.first_name
            initial['last_name'] = self.request.user.last_name
            if 'start' in self.course_info:
                initial['start_support_date'] = parser.parse(self.course_info['start'])
            if 'end' in self.course_info:
                initial['end_project_date'] = parser.parse(self.course_info['end'])
        if self.request.LANGUAGE_CODE:
            initial['country'] = 'Polska'

        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['statuses_options_json'] = json.dumps(STATUSES_OPTIONS, cls=DjangoJSONEncoder)
        context['course_info'] = self.course_info
        return context


@method_decorator(login_required, name='dispatch')
class UserRegistrationCourseView(UserRegistrationCourseViewBase):
    template_name = 'users/form_registration.html'
    success_url = '/thanks/'
    token = None
    course_info = None

    def get_form_class(self):

        if self.request.LANGUAGE_CODE == 'pl':
            return UserRegistrationCourseForm
        return UserRegistrationCourseEnglishForm

    def dispatch(self, request, *args, **kwargs):
        social_token = SocialToken.objects.filter(
            account__user=self.request.user,
            account__provider='edx')

        try:
            self.token = social_token[0].token
        except IndexError:
            return logout(request)

        headers = {
            "Authorization": "Bearer " + self.token
        }

        response = requests.get(
            "{}{}{}".format(
                settings.NAVOICA_URL,
                "/api/courses/v1/courses/",
                self.kwargs['course_id']
            ),
            headers=headers)

        if response.status_code != requests.codes.ok:
            messages.error(request, _("Course does not exist"))
            raise Http404()

        self.course_info = response.json()

        response = requests.get(
            "{}{}{}".format(
                settings.NAVOICA_URL,
                "/api/enrollment/v1/enrollment/",
                self.kwargs['course_id']
            ),
            headers=headers)

        self.success_url = "{}/courses/{}/course/?{}".format(
            settings.NAVOICA_URL,
            self.course_info['course_id'],
            settings.NAVOICA_CAMPAIGN_URL
        )

        course_enrollment = response.json()
        if course_enrollment['is_active'] and not settings.ALLOW_MULTIPLE_REGISTRATION:
            messages.error(request, _("You are already enrolled in this course"))
            raise Http404()

        return super(UserRegistrationCourseView, self).dispatch(request, *args,
                                                                **kwargs)

    def form_valid(self, form):

        headers = {
            "Authorization": "Bearer " + self.token
        }

        requests.post(
            "{}{}".format(
                settings.NAVOICA_URL,
                "/api/enrollment/v1/enrollment",
            ),
            json={
                "course_details": {"course_id": self.course_info['course_id']}},
            headers=headers)

        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.course_id = self.course_info['course_id']
        obj.language_code = self.request.LANGUAGE_CODE
        obj.save()

        logout(self.request)

        return super().form_valid(form)


class UserRegistrationTestView(UserRegistrationCourseViewBase):
    course_info = {
        "course_id": "ABC"
    }

    def get_initial(self):
        initial = super().get_initial()
        initial['email'] = 'test@email.com'
        initial['first_name'] = "Test First"
        initial['last_name'] = "Test Last"
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course_info']['name'] = "Some Test Course Info"
        return context

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user_id = 1
        obj.course_id = self.course_info['course_id']
        obj.language_code = self.request.LANGUAGE_CODE
        obj.save()

        return super().form_valid(form)


class CSVExportViewCustom(CSVExportView):
    def get_field_value(self, obj, field_name):
        """ Override if a custom value or behaviour is required for specific fields. """
        if '__' not in field_name:
            if hasattr(obj, 'all') and hasattr(obj, 'iterator'):
                return ','.join([getattr(ro, field_name) for ro in obj.all()])

            try:
                field = obj._meta.get_field(field_name)
            except FieldDoesNotExist as e:
                if not hasattr(obj, field_name):
                    raise e
                # field_name is a property.
                return getattr(obj, field_name)

            value = field.value_from_object(obj)
            if field.many_to_many:
                return ','.join([six.text_type(ro) for ro in value])
            elif field.choices:
                return value
            return field.value_from_object(obj)
        else:
            related_field_names = field_name.split('__')
            related_obj = getattr(obj, related_field_names[0])
            related_field_name = '__'.join(related_field_names[1:])
            return self.get_field_value(related_obj, related_field_name)

    def get_fields(self, queryset):
        opts = queryset.model._meta
        field_names = [field.name for field in opts.fields]
        field_names += ['navoica_id' ,'navoica_email', 'navoica_username']

        return field_names
