from django.contrib import admin

from .models import ContactFormMessage, Setting

# Register your models here.

class ContactFormMessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'name', 'message')

admin.site.register(ContactFormMessage, ContactFormMessageAdmin)

admin.site.register(Setting)