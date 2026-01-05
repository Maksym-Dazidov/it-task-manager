from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class TaskType(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ['name']
        verbose_name = 'Task Type'
        verbose_name_plural = 'Task Types'

    def __str__(self):
        return self.name


class Position(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ['name']
        verbose_name = 'Position'
        verbose_name_plural = 'Positions'

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        ordering = ['name']
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'

    def __str__(self):
        return self.name


class Worker(AbstractUser):
    position = models.ForeignKey(
        Position,
        on_delete=models.RESTRICT,
        related_name='workers',
        blank=True,
        null=True,
    )

    class Meta:
        ordering = ['username']
        verbose_name = 'Worker'
        verbose_name_plural = 'Workers'

    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name})"

    def get_absolute_url(self):
        return reverse("tasks:worker_detail", kwargs={"pk": self.pk})


class Task(models.Model):
    class PriorityChoices(models.TextChoices):
        URGENT = 'UR', 'Urgent'
        HIGH = 'HI', 'High'
        MEDIUM = 'ME', 'Medium'
        LOW = 'LO', 'Low'

    name = models.CharField(max_length=100)
    description = models.TextField()
    deadline = models.DateTimeField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(
        max_length=2,
        choices=PriorityChoices.choices,
        default=PriorityChoices.MEDIUM,
    )
    task_type = models.ForeignKey(
        TaskType,
        on_delete=models.RESTRICT,
        related_name='tasks_by_type'
    )
    assignees = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='assigned_tasks',
        blank=True,
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='tagged_tasks',
        blank=True,
    )

    class Meta:
        ordering = ['deadline', 'priority']
        verbose_name = 'Task'
        verbose_name_plural = 'Tasks'

    def __str__(self):
        return f"{self.name} ({self.get_priority_display()})"

    def get_absolute_url(self):
        return reverse("tasks:task_detail", kwargs={"pk": self.pk})
