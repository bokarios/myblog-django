from django.contrib import admin
from .models import Post, Comment, Like, Dislike

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    search_fields = ['title', 'content']
    list_display = ('title', 'slug', 'user', 'created_at', 'updated_at')
    list_filter = ('created_at', 'user')


@admin.register(Comment)
class PostAdmin(admin.ModelAdmin):
    search_fields = ['comment']
    list_display = ('user', 'article', 'comment', 'created_at')
    list_filter = ('created_at', 'article', 'user')


@admin.register(Like)
class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'article', 'created_at')
    list_filter = ('created_at', 'article', 'user')


@admin.register(Dislike)
class PostAdmin(admin.ModelAdmin):
    list_display = ('user', 'article', 'created_at')
    list_filter = ('created_at', 'article', 'user')

# admin.site.register(Post)
# admin.site.register(Comment)
# admin.site.register(Like)
# admin.site.register(Dislike)
