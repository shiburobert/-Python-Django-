from django.contrib import admin
from .models import * 
admin.site.register(Catagory)
admin.site.register(Product)
admin.site.register(Order)

from django.contrib import admin
from .models import ContactMessage

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'submitted_at')
    search_fields = ('name', 'email')
