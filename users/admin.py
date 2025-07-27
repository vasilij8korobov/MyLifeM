from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username',)
    fieldsets = (
        *UserAdmin.fieldsets,
        ('Дополнительная информация', {'fields': ('avatar',),
                                       'classes': ('collapse',)}),
    )
