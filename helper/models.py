from django.contrib.auth.models import User
from django.db import models


class Problem(models.Model):
    STATUS_CHOICES = (
        ('new', 'New'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('confirmed', 'Confirmed')
    )

    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    action = models.TextField(null=True, blank=True)
    resolved_user = models.ForeignKey(User, related_name='resolved_problems', on_delete=models.SET_NULL, null=True,
                                      blank=True)


    def __str__(self):
        return self.title


class UserAction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    action = models.TextField()

    def __str__(self):
        return f"{self.user.username} - {self.problem.title}"
