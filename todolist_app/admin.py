from django.contrib import admin

from todolist_app.models import TaskList


@admin.register(TaskList)
class TaskListAdmin(admin.ModelAdmin):
    pass
