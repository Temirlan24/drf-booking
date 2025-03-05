from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    department = models.CharField(max_length=100, blank=True, null=True)
    position = models.CharField(max_length=100, blank=True, null=True)
    employee_id = models.CharField(max_length=50, unique=True, blank=True, null=True)

    def __str__(self):
        return self.username

class Room(models.Model):
    name = models.CharField(max_length=100)
    room_location = models.CharField(max_length=100)
    capacity = models.PositiveIntegerField()
    equipment = models.TextField(blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

class Booking(models.Model):
    STATUS_CHOICES = [
        ('confirmed', 'подтверждено'),
        ('cancelled', 'отменено'),
        ('completed', 'завершено'),
    ]

    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='confirmed')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Booking by {self.user.username} for {self.room.name}"