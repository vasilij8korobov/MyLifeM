from django.contrib import admin
from .models import DiaryEntry, Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color')
    list_editable = ('color',)
    search_fields = ('name',)


class DiaryEntryAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'date', 'updated_at', 'is_private')
    list_filter = ('is_private', 'date', 'user')
    search_fields = ('title', 'text', 'user__username')
    readonly_fields = ('date', 'updated_at')
    date_hierarchy = 'date'

    fieldsets = (
        (None, {
            'fields': ('user', 'title', 'text')
        }),
        ('Настройки видимости', {
            'fields': ('is_private',)
        }),
        ('Метаданные', {
            'fields': ('date', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


admin.site.register(DiaryEntry, DiaryEntryAdmin)
