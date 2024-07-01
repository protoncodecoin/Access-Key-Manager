from django.contrib import admin
from django.contrib import messages

from .models import AccessKey

# Register your models here.


def revoke_keys(modeladmin, request, queryset):
    """
    Revoke a list of selected keys on the admin site
    """
    for obj in queryset:
        if obj.status == AccessKey.Status.ACTIVE:
            obj.status = AccessKey.Status.REVOKED
            obj.save()
    messages.success(request, "Key(s) Revoked successfully")


revoke_keys.short_description = "Revoke Keys"


def active_keys(modeladmin, request, queryset):
    """
    Active a list of selected keys on the admin site
    """
    for obj in queryset:
        if obj.status != AccessKey.Status.ACTIVE:
            obj.status = AccessKey.Status.ACTIVE
            obj.save()
    messages.success(request, "Key(s) Actived successfully")


active_keys.short_descripton = "Active Keys"


@admin.register(AccessKey)
class KeyManagerAdmin(admin.ModelAdmin):
    """
    Customize fields displayed on the admin site
    """

    list_display = [
        "user",
        "key",
        "status",
        "procurement_date",
        "expiry_date",
    ]
    list_filter = [
        "status",
        "procurement_date",
        "expiry_date",
    ]
    ordering = [
        "status",
        "expiry_date",
        "procurement_date",
    ]
    show_facets = admin.ShowFacets.ALWAYS
    actions = [revoke_keys, active_keys]
