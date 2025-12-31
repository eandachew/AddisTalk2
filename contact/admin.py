
from django.contrib import admin
from .models import ContactMessage

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'name', 'email', 'created_on', 'is_read', 'resolved')  
    list_filter = ('is_read', 'resolved', 'created_on')  
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('created_on',) 
    list_per_page = 20
    actions = ['mark_as_read', 'mark_as_resolved']
    
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)
        self.message_user(request, f"{queryset.count()} messages marked as read.")
    mark_as_read.short_description = "Mark selected messages as read"
    
    def mark_as_resolved(self, request, queryset):
        queryset.update(resolved=True, is_read=True)
        self.message_user(request, f"{queryset.count()} messages marked as resolved.")
    mark_as_resolved.short_description = "Mark selected messages as resolved"
