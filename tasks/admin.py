from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from tasks.models import TaskType, Position, Tag, Worker, Task


@admin.register(TaskType)
class TaskTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Worker)
class WorkerAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ('position',)
    list_filter = UserAdmin.list_filter + ('position',)
    search_fields = UserAdmin.search_fields + ('position__name',)
    fieldsets = UserAdmin.fieldsets + (
        (("Additional Information", {'fields': ("position",)}),)
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (("Additional Information", {'fields': ("position", "first_name", "last_name", "email",)}),)
    )


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'deadline',
        'is_completed',
        'priority',
        'task_type',
        'display_assignees',
    )
    list_filter = (
        'is_completed',
        'priority',
        'task_type',
        'assignees',
        'tags',
    )
    search_fields = (
        'name',
        'description',
        'assignees__username'
    )
    fieldsets = (
        ("Core Task Details", {
            'fields': ("name", "description"),
            'description': "Provide a clear name and detailed description for the task."
        }),
        ("Classification and Scheduling", {
            'fields': ("task_type", "priority", "deadline"),
        }),
        ("Team and Context", {
            'fields': ("assignees", "tags"),
            'classes': ('collapse',),
        }),
        ("Status", {
            'fields': ("is_completed",),
        })
    )

    def display_assignees(self, obj):
        return ', '.join(
            obj.assignees.values_list('username', flat=True)
        )

    display_assignees.short_description = 'Assignees'
