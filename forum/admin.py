from django.contrib import admin

from .models import Post
from .models import Comment

# Define Admin model classes for admin page

class PostAdmin(admin.ModelAdmin):
     list_display = ['title','date','author']

class CommentAdmin(admin.ModelAdmin):
     list_display = ['post','date','author']
     

admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)
