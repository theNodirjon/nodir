from django.contrib import admin
from accounts.models import User
# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name',  'is_email_verified', 'is_active')
    search_fields = ['email']