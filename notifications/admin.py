from .models import EmailNotification
from django.contrib import admin
from .models import Device


class DeviceAdmin(admin.ModelAdmin):
    list_display = ('user', 'token', 'created_at')
    list_display_links = ('user', 'token')
    search_fields = ('user__name', 'token')


admin.site.register(Device, DeviceAdmin)


@admin.register(EmailNotification)
class EmailNotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'receive_email_notifications', 'created_at')
    search_fields = ('user__email',)
    list_filter = ('receive_email_notifications',)
