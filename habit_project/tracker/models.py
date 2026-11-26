from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class HabitLog(models.Model):
    habit = models.ForeignKey(Habit, on_delete=models.CASCADE, related_name='logs')
    date = models.DateField(default=timezone.now)

    class Meta:
        unique_together = ('habit', 'date') 

    def __str__(self):
        return f"{self.habit.title} - {self.date}"