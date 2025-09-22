from django.contrib import admin
from .models import Post, Comment

# Register your models here.
# admin.site.register(Post)

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'publish', 'status']
    list_filter = ['slug', 'status', 'created', 'publish']
    search_fields = ['title', 'body']
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ['author']
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']
    show_facets = admin.ShowFacets.ALWAYS


@admin.register(Comment)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'body', 'created', 'post', 'active']
    list_filter = ['active', 'created', 'updated']
    search_fields = ['name', 'email', 'body']
    
    