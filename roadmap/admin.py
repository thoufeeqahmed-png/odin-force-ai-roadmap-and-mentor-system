from django.contrib import admin
from .models import Roadmap, RoadmapStage, LearningTask


class LearningTaskInline(admin.TabularInline):
    model = LearningTask
    extra = 1
    fields = ('order', 'task_type', 'title', 'completed', 'description')


class RoadmapStageInline(admin.StackedInline):
    model = RoadmapStage
    extra = 0
    show_change_link = True
    fields = ('order', 'title', 'estimated_duration', 'description', 'why_it_matters', 'what_to_practice', 'suggested_projects')


@admin.register(Roadmap)
class RoadmapAdmin(admin.ModelAdmin):
    list_display = ('domain', 'goal', 'current_level', 'user_name', 'available_time', 'duration', 'progress_percentage_display', 'created_at')
    list_filter = ('current_level', 'created_at', 'domain')
    search_fields = ('domain', 'goal', 'user_name', 'existing_skills')
    inlines = [RoadmapStageInline]

    def progress_percentage_display(self, obj):
        return f"{obj.progress_percentage}%"
    progress_percentage_display.short_description = "Progress"


@admin.register(RoadmapStage)
class RoadmapStageAdmin(admin.ModelAdmin):
    list_display = ('title', 'roadmap', 'order', 'estimated_duration', 'tasks_count_display')
    list_filter = ('roadmap__domain',)
    search_fields = ('title', 'description', 'why_it_matters')
    inlines = [LearningTaskInline]

    def tasks_count_display(self, obj):
        return f"{obj.completed_tasks_count}/{obj.total_tasks_count} completed"
    tasks_count_display.short_description = "Tasks"


@admin.register(LearningTask)
class LearningTaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'stage', 'task_type', 'completed', 'order')
    list_filter = ('task_type', 'completed', 'stage__roadmap__domain')
    search_fields = ('title', 'description', 'stage__title')
    list_editable = ('completed',)
