from django.utils.translation import ugettext_lazy as _
from django_countries.data import COUNTRIES

STATUSES_OPTIONS = {
    'employed': [
        _("A person working in the government administration"),
        _("A person working in local government administration"),
        _("other"),
        _("A person works in MSME"),
        _("A person working in a non-governmental administration"),
        _("A self-employed person"),
        _("A person working in a large enterprise")
    ],
    'registered': [
        _("Long-term unemployed person"),
        _("other")
    ],
    'unregistered': [
        _("Long-term unemployed person"),
        _("other")
    ],
    'looking': [
        _("Learning"),
        _("A person not participating in education or training"),
        _("other")
    ]

}
COUNTRIES_ENROLL = [
                       ('', _('Select...')),
                   ] + list(COUNTRIES.items())

COUNTRIES_ENROLL.append(('ZZ', _('Unknown or unspecified country')))
