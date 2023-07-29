from django.contrib import admin
from .models import News , Category , Contact , Comment
# Register your models here.

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title' ,'content' , 'publish_time' , 'status']
    list_filter = ['status' , 'created_time' ,'publish_time']
    date_hierarchy = 'publish_time'
    search_fields = ['title' , 'body']
    ordering = ['status' , 'publish_time']
    prepopulated_fields = {'slug': ('content',)}

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id' , 'name']
    list_filter = ['name']
    search_fields = ['name']
    prepopulated_fields = {'slug_ctg':('name',)}

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name' , 'email']
    list_filter = ['name']
    search_fields = ['name' , 'email']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user' , 'body' , 'created_time' , 'active']
    list_filter = ['active', 'created_time']
    search_fields = ['user' , 'body']
    actions = ['disable_comments' , 'activate_comments']
    def disable_comments(self , request , queryset):
        queryset.update(active = False)
    def activate_comments(self , request , queryset):
        queryset.update(active = True)
