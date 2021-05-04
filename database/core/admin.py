from django.contrib import admin
from .models import Snapshot

# Register your models here.

class SnapshotAdmin(admin.ModelAdmin):
    list_display = ['title','image_tag','verified','date_created']
    list_filter = ['title','verified','date_created']
    search_fields = ['title','verified','date_created']
    
admin.site.register(Snapshot, SnapshotAdmin)
