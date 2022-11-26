from django.contrib import admin
from .models import create_ranking,Post_rank,Post_coment

class create_rankingAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'element')
    list_display_links = ('id', 'title')
admin.site.register(create_ranking, create_rankingAdmin)

class Post_rankAdmin(admin.ModelAdmin):
    list_display = ('id', 'Post_name', 'Post_element')
    list_display_links = ('id', 'Post_name')
admin.site.register(Post_rank, Post_rankAdmin)

class Post_comentAdmin(admin.ModelAdmin):
    list_display = ('id', 'Post_coment_name', 'Post_coment_text')
    list_display_links = ('id', 'Post_coment_name')
admin.site.register(Post_coment, Post_comentAdmin)
