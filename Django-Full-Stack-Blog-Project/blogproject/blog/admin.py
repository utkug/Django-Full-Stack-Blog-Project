from django.contrib import admin
from . models import Author, Post, Tag, Comment, Room, Message  
# Register your models here.

class PostAdmin(admin.ModelAdmin):

    list_filter =  ("author", "tags", "date")
    list_display = ("title","date","author")
    prepopulated_fields = {"slug":("title",)} #also u can add more

class CommentAdmin(admin.ModelAdmin):
    list_display =("user_name","text","date")

admin.site.register(Author)
admin.site.register(Post, PostAdmin)
admin.site.register(Tag)
admin.site.register(Comment, CommentAdmin)


admin.site.register(Room)
admin.site.register(Message)