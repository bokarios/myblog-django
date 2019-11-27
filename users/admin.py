from django.contrib import admin
from .models import Profile

@admin.register(Profile)
class PostAdmin(admin.ModelAdmin):
    search_fields = ['address']
    list_display = ('user','address', 'created_at', 'updated_at')
    list_filter = ('created_at',)

# admin.site.register(Profile)
