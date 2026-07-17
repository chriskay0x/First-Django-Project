from django.contrib import admin
from .models import Task

# Register your models here.
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'due_time')
    search_fields = ('id', 'title')
    list_filter = ('due_time',)

admin.site.register(Task, TaskAdmin)

 