from django.contrib import admin
from .models import comenting

class comentingAdmin(admin.ModelAdmin):
    list_display = ('id','coment_text',)
    list_display_links = ('id', 'coment_text')
admin.site.register(comenting,comentingAdmin)
