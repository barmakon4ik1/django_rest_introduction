from django.db import models
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import User
from django.utils import timezone

from projects.models import Project


class Tag(models.Model):
    name = models.CharField(max_length=20, validators=[MinLengthValidator(4)])

    def __str__(self):
        return self.name


class Tasks(models.Model):
    STATUS_CHOICES = (
        ('NEW', 'new'),
        ('PENDING', 'pending'),
        ('IN PROGRESS', 'in progress'),
        ('DONE', 'done'),
    )
    name = models.CharField(max_length=120)
    description = models.TextField()
    status = models.CharField(max_length=13, choices=STATUS_CHOICES, default='new')
    assignee = models.ForeignKey(to=User, on_delete=models.PROTECT, related_name='tags', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField(to='Tag', related_name='tasks')
    project = models.ForeignKey(to='Project', on_delete=models.CASCADE related_name='tasks')
    deadline = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-deadline']

