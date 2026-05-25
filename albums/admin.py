from django.contrib import admin
from .models import Album, Photo


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('title', 'owner', 'created_at')
    search_fields = ('title', 'description', 'owner__username')
    list_filter = ('created_at',)


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('title', 'album', 'created_at')
    search_fields = ('title', 'caption', 'album__title')
    list_filter = ('created_at',)
