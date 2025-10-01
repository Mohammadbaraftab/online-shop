from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserChangeForm, UserCreationForm
from.models import User, OtpCode


@admin.register(OtpCode)
class OtpCodeAdmin(admin.ModelAdmin):
    list_display = ("phone_number", "code", "created")


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ("email", "phone_number", "is_admin")
    list_filter = ("is_admin", )
    fieldsets = (
        ("Main", {"fields": ("phone_number", "email", "full_name", "password")}),
        ("permissions", {"fields":("is_admin",)})
    )

    add_fieldsets = (
        (None, {"fields":("phone_number", "email", "full_name", "password1", "password2")}),
    )

    search_fields = ("email", "full_name")
    ordering = ("email", )
    filter_horizontal = ()
    
admin.site.unregister(Group)
admin.site.register(User, UserAdmin)