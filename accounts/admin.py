from django.contrib import admin
from .models import User
# Register your models here.

class UserAdmin(admin.ModelAdmin):
	list_display = ['pk', 'username','email','date_joined','is_staff','is_active']
	list_display_link = ['pk', 'username','email','date_joined','is_staff','is_active']

admin.site.register(User, UserAdmin)