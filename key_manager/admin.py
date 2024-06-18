from django.contrib import admin

from .models import KeyManager
# Register your models here.

@admin.register(KeyManager)
class KeyManagerAdmin(admin.ModelAdmin):
    """
    Customize fields displayed on the admin site
    """
    list_display = [
        'user',
        'key',
        'status',
        "procurement_date",
        "expiry_date",
    ]
    list_filter = [
        'status', 'procurement_date', 'expiry_date',
    ]
    ordering = ['status', 'expiry_date', 'procurement_date',]
    show_facets = admin.ShowFacets.ALWAYS
