from django.contrib import admin
from .models import Post, Comment, Like, Newsletter

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_date', 'published_date')
    list_filter = ('created_date', 'published_date')
    search_fields = ('title', 'content')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'author', 'created_date')
    list_filter = ('approved_comment', 'created_date')
    search_fields = ('post', 'author')


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'created_date')

@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_date', 'is_active')
    list_filter = ('is_active', 'subscribed_date')
    search_fields = ('email',)
