from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
from .models import User

class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('username','password')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser',
                                        )}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )



admin.site.register(User, UserAdmin)
