from crispy_forms.helper import FormHelper
from crispy_forms.layout import ButtonHolder, Div, Fieldset, HTML, Layout, \
    Submit
from django.conf import settings
from django.contrib.auth import forms, get_user_model
from django.core.exceptions import ValidationError
from django.forms import BooleanField, EmailField, ModelForm, TextInput, CharField, RadioSelect, Select
from django.forms.fields import RegexField
from django.templatetags.static import static
from django.utils.translation import ugettext_lazy as _
from localflavor.pl.forms import PLPESELField

from .models import UserRegistrationCourse

User = get_user_model()


class UserChangeForm(forms.UserChangeForm):
    class Meta(forms.UserChangeForm.Meta):
        model = User


class UserCreationForm(forms.UserCreationForm):
    error_message = forms.UserCreationForm.error_messages.update(
        {"duplicate_username": _("This username has already been taken.")}
    )

    class Meta(forms.UserCreationForm.Meta):
        model = User

    def clean_username(self):
        username = self.cleaned_data["username"]

        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username

        raise ValidationError(self.error_messages["duplicate_username"])


class UserRegistrationCourseFormBase(ModelForm):
    pesel = PLPESELField(max_length=11, label=_("PESEL"), widget=TextInput(attrs={'type': 'number'}), required=False)
    postal_code = RegexField(label=_("Postal code"), regex=r"(?i)^[a-z0-9][a-z0-9\- ]{0,10}[a-z0-9]$")
    email = EmailField(label=_("E-mail address"))

    phone = CharField(label=_("Phone"), max_length=30)

    status_info = CharField(required=False, label=_("Status additional information"), widget=Select())

    statement1 = BooleanField(required=True)
    statement2 = BooleanField(required=True)

    def __init__(self, *args, **kwargs):
        super(UserRegistrationCourseFormBase, self).__init__(*args, **kwargs)
        print("OKOOKO")

        self.fields['statement1'].label = _(
            "I agree with <a href='{url}' target='_blank'>the project participant's declaration.</a>").format(
            url=
            static(settings.STATEMENT1_PDF))

        self.fields['statement2'].label = _(
            "I consent to <a href='{url}' target='_blank'>the processing of my personal data to participate in the project.</a>").format(
            url=
            static(settings.STATEMENT2_PDF))

        self.fields['homeless'].choices = list(filter(lambda x: x[0] != 'r', self.fields['homeless'].choices))

        self.helper = FormHelper(self)

        self.helper.layout = Layout(
            Fieldset(
                '',
                Div(
                    HTML('<div class="col-lg-4 pl-lg-0 px-0"><h3 class="h4 mx-0">{}</h3></div>'.format(
                        _("Participant details"))),
                    Div(
                        Div(
                            Div('first_name',
                                css_class="col-md-6 register-course__input-container"
                                ),
                            Div(
                                'last_name',
                                css_class="col-md-6 register-course__input-container"
                            ),
                            css_class="row"
                        ),
                        Div(
                            Div('citizenship',
                                css_class="col-md-6 register-course__input-container"
                                ),
                            Div(
                                'pesel',
                                css_class="col-md-6 register-course__input-container"
                            ),
                            css_class="row"
                        ),

                        Div(
                            Div('gender',
                                css_class="col-md-3 register-course__input-container"
                                ),
                            Div(
                                'age',
                                css_class="col-md-3 register-course__input-container"
                            ),
                            Div('education',
                                css_class="col-md-6 register-course__input-container"
                                ),
                            css_class="row"
                        ),
                        css_class="group col-lg-8 ml-lg-auto px-0"
                    ), css_class="d-flex flex-wrap"),
                Div(
                    HTML('<hr class="w-100 pb-40" />'),
                    HTML('<div class="col-lg-4 pl-lg-0 px-0"><h3 class="h4 mx-0 w-67">{}</h3></div>'.format(
                        _("Contact details / Postal address"))),
                    Div(
                        Div(
                            Div('phone',
                                css_class="col-md-6 register-course__input-container"
                                ),
                            Div(
                                'email',
                                css_class="col-md-6 register-course__input-container"
                            ),
                            css_class="row"
                        ),
                        Div(
                            Div('street',
                                css_class="col-md-6 register-course__input-container"
                                ),
                            Div('street_no',
                                css_class="col-md-3 register-course__input-container"
                                ),
                            Div(
                                'street_building_no',
                                css_class="col-md-3 register-course__input-container"
                            ),
                            Div(
                                'postal_code',
                                css_class="col-md-6 register-course__input-container"
                            ),
                            Div('city',
                                css_class="col-md-6 register-course__input-container"
                                ),
                            css_class="row"
                        ),
                        Div(
                            Div(
                                'country',
                                css_class="col-md-6 register-course__input-container"
                            ),
                            Div(
                                'voivodeship',
                                css_class="col-md-6 register-course__input-container"
                            ),
                            Div(
                                'county',
                                css_class="col-md-6 register-course__input-container"
                            ),
                            Div(
                                'commune',
                                css_class="col-md-6 register-course__input-container"
                            ),
                            css_class="row"
                        ),
                        css_class="group col-lg-8 ml-lg-auto px-0"
                    ), css_class="d-flex flex-wrap"),
                Div(
                    HTML('<hr class="w-100 pb-40" />'),
                    HTML('<div class="col-lg-4 pl-lg-0 px-0"><h3 class="h4 mx-0">{}</h3></div>'.format(
                        _("Additional information"))),
                    Div(
                        Div(
                            Div('status',
                                css_class="col-md-12 register-course__input-container"
                                ),
                            Div('status_info',
                                css_class="col-md-12 register-course__input-container"
                                ),
                            Div(
                                'profession',
                                css_class="col-md-6 register-course__input-container"
                            ),
                            Div(
                                'work_name',
                                css_class="col-md-6 register-course__input-container"
                            ),
                            css_class="row"
                        ),
                        Div(
                            Div('start_project_date',
                                css_class="col-md-12 register-course__input-container"
                                ),
                            Div(
                                'end_project_date',
                                css_class="col-md-12 register-course__input-container"
                            ),
                            Div(
                                'start_support_date',
                                css_class="col-md-12 register-course__input-container"
                            ),
                            css_class="row d-none"
                        ),
                        Div(
                            Div('origin',
                                css_class="col-md-12 register-course__input-container"
                                ),
                            Div(
                                'homeless',
                                css_class="col-md-12 register-course__input-container"
                            ),
                            Div(
                                'disabled_person',
                                css_class="col-md-12 register-course__input-container"
                            ),
                            Div(
                                'social_disadvantage',
                                css_class="col-md-12 register-course__input-container"
                            ),
                            css_class="row align-items-end"
                        ),
                        css_class="group col-lg-8 ml-lg-auto px-0"
                    ), css_class="d-flex flex-wrap"),

            ),
            Div(
                HTML('<hr class="w-100 pb-40" />'),
                HTML('<div class="col-lg-4 pl-lg-0 px-0"><h3 class="h4 mx-0">{}</h3></div>'.format(
                    _("Required consents"))),
                Div(
                    'statement1', 'statement2',
                    css_class="group mb-md-5 mb-4  col-lg-8 ml-lg-auto px-0"
                ), css_class="d-flex flex-wrap"),
            Div(
                HTML('<hr class="w-100 pb-30 my-0" />'),
                Div(
                    HTML(
                        '<div class="col-lg-2 col-xs-12 col-md-3 mr-lg-auto order-3 order-md-1 d-flex"><img src="/static/images/logo-navoica.svg" alt="Logo Navoica.pl" class="navoica-logo img-fluid align-self-center" /></div>'),
                    Div(
                        HTML('<button class="btn btn-cancel rounded-0 mr-lg-5 mr-md-2 d-none">{}</button>'.format(
                            _("Cancel"))),
                        ButtonHolder(
                            Submit('submit',
                                   _("Register me for the course"),
                                   css_class='button white w-100 rounded-0 btn-submit')
                        ),
                        css_class='form-buttons d-flex flex-wrap oder-1 order-md-2 justify-content-between flex-column flex-md-row'),
                    css_class='d-flex justify-content-between flex-wrap align-items-center'
                )),
        )

    class Meta:
        model = UserRegistrationCourse
        exclude = ('user', 'course_id', 'language_code')
        widgets = {
            'origin': RadioSelect(
                attrs={'required': 'required'}),
            'homeless': RadioSelect(
                attrs={'required': 'required'}),
            'disabled_person': RadioSelect(
                attrs={'required': 'required'}),
            'social_disadvantage': RadioSelect(
                attrs={'required': 'required'})
        }


class UserRegistrationCourseForm(UserRegistrationCourseFormBase):
    pass


class UserRegistrationCourseEnglishForm(UserRegistrationCourseFormBase
                                        ):
    def __init__(self, *args, **kwargs):
        super(UserRegistrationCourseEnglishForm, self).__init__(*args, **kwargs)
        self.fields['pesel'].required = False
        self.fields['voivodeship'].required = False
        self.fields['county'].required = False
        self.fields['commune'].required = False

        self.fields['statement1'].label = _(
            "I agree with <a href='{url}' target='_blank'>the project participant's declaration.</a>").format(
            url=
            static(settings.STATEMENT1_EN_PDF))

        self.fields['statement2'].label = _(
            "I consent to <a href='{url}' target='_blank'>the processing of my personal data to participate in the project.</a>").format(
            url=
            static(settings.STATEMENT2_EN_PDF))
