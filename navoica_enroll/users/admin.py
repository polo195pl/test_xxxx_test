from django.contrib import admin
from django.contrib.auth import admin as auth_admin, get_user_model
from django.utils.translation import ugettext_lazy as _

from navoica_enroll.users.forms import UserChangeForm, UserCreationForm
from navoica_enroll.users.models import UserRegistrationCourse
from navoica_enroll.users.views import CSVExportViewCustom

User = get_user_model()

admin.site.site_title = _("Registration form")
admin.site.site_header = _("Registration form")
admin.site.index_title = _(
    "Registration form for users of courses implemented with co-financing from the ESF, NCBR funds")


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    fieldsets = (("User",
                  {"fields": ("name",)}),) + auth_admin.UserAdmin.fieldsets
    list_display = ["username", "name", "is_superuser"]
    search_fields = ["name"]


@admin.register(UserRegistrationCourse)
class UserRegistrationCourseAdmin(admin.ModelAdmin):
    actions = ('export_data_csv',)
    list_display = ["first_name", "last_name", 'gender', "course_id", "language_code"]
    list_filter = ('course_id', "start_project_date", "end_project_date", "start_support_date")

    def export_data_csv(self, request, queryset):
        view = CSVExportViewCustom(queryset=queryset, fields='__all__')
        return view.get(request)

    export_data_csv.short_description = _('Export CSV')
