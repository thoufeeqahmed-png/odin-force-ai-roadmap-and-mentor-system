from django.db import models
from django.urls import reverse


class Roadmap(models.Model):
    LEVEL_CHOICES = [
        ('Complete Beginner', 'Complete Beginner (Brand new to the field)'),
        ('Beginner', 'Beginner (Basic familiarity / know fundamentals)'),
        ('Intermediate', 'Intermediate (Hands-on experience, looking to level up)'),
        ('Advanced', 'Advanced (Deep experience, looking for mastery/specialization)'),
    ]

    MENTOR_CHOICES = [
        ('odin', 'ODIN - Wise & Strategic (Long-term goals, career planning, leadership)'),
        ('thor', 'THOR - Motivating & Action-focused (Practical skills, projects, execution)'),
        ('loki', 'LOKI - Creative & Problem-solving (Creative subjects, innovation, alternatives)'),
        ('auto', 'Auto-select based on domain'),
    ]

    domain = models.CharField(max_length=200, help_text="e.g. Artificial Intelligence, Photography, Finance")
    current_level = models.CharField(max_length=50, choices=LEVEL_CHOICES, default='Beginner')
    goal = models.CharField(max_length=300, help_text="e.g. Become an AI Engineer, Start a Portrait Studio")
    available_time = models.CharField(max_length=100, default='2 hours per day', help_text="e.g. 1 hour per day, 2 hours per day, 10 hours/week")
    duration = models.CharField(max_length=100, default='6 months', help_text="e.g. 3 months, 6 months, 1 year")
    existing_skills = models.TextField(blank=True, default='', help_text="Skills or tools you already know")
    user_name = models.CharField(max_length=100, blank=True, default='Learner', help_text="Your name or nickname")
    mentor = models.CharField(max_length=20, choices=MENTOR_CHOICES, default='auto', help_text="Your mentor guide for this roadmap")
    
    # Generated AI metadata and supportive persona advice
    greeting_message = models.TextField(blank=True, default='')
    junior_advice = models.TextField(blank=True, default='')
    mentor_greeting = models.TextField(blank=True, default='', help_text="Personalized mentor greeting")
    roadmap_content = models.TextField(blank=True, default='', help_text="Full structured overview / raw backup")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.domain} Roadmap: {self.goal} ({self.current_level})"

    def get_absolute_url(self):
        return reverse('roadmap_detail', kwargs={'pk': self.pk})

    @property
    def total_tasks(self):
        return LearningTask.objects.filter(stage__roadmap=self).count()

    @property
    def completed_tasks(self):
        return LearningTask.objects.filter(stage__roadmap=self, completed=True).count()

    @property
    def progress_percentage(self):
        total = self.total_tasks
        if total == 0:
            return 0
        return int((self.completed_tasks / total) * 100)

    @property
    def total_projects(self):
        return LearningTask.objects.filter(stage__roadmap=self, task_type='project').count()

    @property
    def completed_projects(self):
        return LearningTask.objects.filter(stage__roadmap=self, task_type='project', completed=True).count()

    @property
    def total_topics(self):
        return LearningTask.objects.filter(stage__roadmap=self, task_type='topic').count()

    @property
    def completed_topics(self):
        return LearningTask.objects.filter(stage__roadmap=self, task_type='topic', completed=True).count()

    @property
    def current_stage(self):
        """Returns the first stage that is not 100% complete, or the last stage."""
        stages = list(self.stages.all())
        if not stages:
            return None
        for stage in stages:
            if not stage.is_completed:
                return stage
        return stages[-1]

    @property
    def next_daily_task(self):
        """Returns the next incomplete task for daily guidance."""
        task = LearningTask.objects.filter(stage__roadmap=self, completed=False).order_by('stage__order', 'order').first()
        if task:
            return task
        return LearningTask.objects.filter(stage__roadmap=self).order_by('stage__order', 'order').first()

    @property
    def daily_practice_task(self):
        """Returns an actionable practice task for the current focus."""
        curr_stage = self.current_stage
        if curr_stage:
            practice_task = curr_stage.tasks.filter(task_type='practice', completed=False).order_by('order').first()
            if practice_task:
                return practice_task
        return None


class RoadmapStage(models.Model):
    roadmap = models.ForeignKey(Roadmap, on_delete=models.CASCADE, related_name='stages')
    title = models.CharField(max_length=255, help_text="e.g. Stage 1 — Foundations")
    description = models.TextField(help_text="Overview of this stage")
    why_it_matters = models.TextField(help_text="Why this stage is crucial for the goal")
    what_to_practice = models.TextField(blank=True, default='', help_text="Key drills and hands-on exercises")
    suggested_projects = models.TextField(blank=True, default='', help_text="Portfolio-worthy projects")
    order = models.PositiveIntegerField(default=1)
    estimated_duration = models.CharField(max_length=100, default='4 weeks', help_text="e.g. Weeks 1-4")
    projects_summary = models.TextField(blank=True, default='')

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.title} ({self.roadmap.domain})"

    @property
    def total_tasks_count(self):
        return self.tasks.count()

    @property
    def completed_tasks_count(self):
        return self.tasks.filter(completed=True).count()

    @property
    def progress_percentage(self):
        total = self.total_tasks_count
        if total == 0:
            return 0
        return int((self.completed_tasks_count / total) * 100)

    @property
    def is_completed(self):
        total = self.total_tasks_count
        if total == 0:
            return False
        return self.completed_tasks_count == total


class LearningTask(models.Model):
    TASK_TYPES = [
        ('topic', 'Core Topic / Concept'),
        ('practice', 'Hands-on Practice Drill'),
        ('project', 'Real-world Project / Milestone'),
    ]

    stage = models.ForeignKey(RoadmapStage, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, default='')
    task_type = models.CharField(max_length=20, choices=TASK_TYPES, default='topic')
    completed = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['order']

    def __str__(self):
        status = "[x]" if self.completed else "[ ]"
        return f"{status} ({self.task_type}) {self.title}"
