
from django.contrib import admin
from allauth.account.models import EmailAddress

try:
    admin.site.unregister(EmailAddress)
except admin.sites.NotRegistered:
    pass

@admin.register(EmailAddress)
class EmailAddressAdmin(admin.ModelAdmin):
    list_display = ('email', 'user', 'verified', 'primary')
    list_filter = ('verified', 'primary')
    search_fields = ('email', 'user__username', 'user__email')
    ordering = ('-verified', 'email')