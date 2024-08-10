from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

class UserAdmin(BaseUserAdmin):
    model = User
    fieldsets = (
        (None, {'fields': ('username', 'password',)}),
        ('Personal info', {'fields': ('email',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'regisered')}
        ),
    )
    list_display = ('username', 'email','registered')
    search_fields = ('username', 'email',)
    ordering = ('username',)

admin.site.register(User, UserAdmin)