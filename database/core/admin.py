from django.contrib import admin
from .models import Snapshot

# Register your models here.

class SnapshotAdmin(admin.ModelAdmin):
    list_display = ['title','image_tag',]
    list_filter = ['title']
    search_fields = ['title']
    
admin.site.register(Snapshot, SnapshotAdmin)
