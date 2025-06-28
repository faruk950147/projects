from django.contrib import admin
from django.contrib.auth.models import Group
from account.models import User, Profile

admin.site.unregister(Group)

class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'email', 'is_staff', 'is_superuser', 'is_active', 'last_login', 'joined_date']
    list_display_links = ['id', 'username', 'email', 'is_staff', 'is_superuser', 'is_active', 'last_login', 'joined_date']
    readonly_fields = ['password']
    #list_editable = ['is_staff', 'is_superuser', 'is_active']
admin.site.register(User, UserAdmin)

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'username', 'full_name', 'image_tag', 'country', 'city', 'home_city', 'zip_code', 'phone', 'address1', 'address2', 'is_email_verified', 'email_token', 'joined_date']
    list_display_links = ['id', 'user', 'username', 'full_name', 'image_tag', 'country', 'city', 'home_city', 'zip_code', 'phone', 'address1', 'address2', 'is_email_verified', 'email_token', 'joined_date']
    #list_editable = ['is_email_verified']
admin.site.register(Profile, ProfileAdmin)