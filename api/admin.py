from django.contrib import admin

from api.models import Follow


@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ['user', 'following']
