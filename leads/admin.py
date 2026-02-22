from django.contrib import admin
from .models import Lead


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'phone_number', 'assigned_to', 'status', 'color_code', 'created_at')
    list_filter = ('status', 'color_code', 'assigned_to', 'created_at')
    search_fields = ('first_name', 'last_name', 'phone_number', 'email', 'remarks')
