from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'phone', 'birth_date')
    fieldsets = (
        *UserAdmin.fieldsets,
        ('Дополнительная информация', {'fields': ('phone', 'avatar', 'birth_date'),
                                       'classes': ('collapse',)}),
    )

    add_fieldsets = (
        *UserAdmin.add_fieldsets,
        (
            'Дополнительные данные',
            {
                'fields': ('phone', 'birth_date'),
                'classes': ('collapse',)
            }
        )
    )