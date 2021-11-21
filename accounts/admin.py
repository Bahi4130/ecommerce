from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from accounts.models import Account


class AccountAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'username', 'last_login', 'date_joined', 'is_active',)
    list_display_links = ('email', 'last_name')
    search_fields = ('email', 'last_name')
    readonly_fields = ('date_joined', 'last_login',)
    ordering = ('-date_joined',)
    fieldsets = ()

    filter_horizontal = ()
    list_filter = ()


admin.site.register(Account, AccountAdmin)
