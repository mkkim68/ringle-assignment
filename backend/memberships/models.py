from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import AbstractUser

class Company(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

class User(AbstractUser):
    ROLE_CHOICES = (
        ('user', 'User'),
        ('admin', 'Admin'),
        ('b2b', 'B2B')
    )
    name = models.CharField(max_length=50)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.username


class MembershipType(models.Model):
    name = models.CharField(max_length=100)
    valid_days = models.PositiveIntegerField()
    conversation_limit = models.IntegerField()  # -1: 무제한
    analysis_limit = models.IntegerField()  # -1: 무제한
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True)  # B2B용 멤버십일때
    
    def __str__(self):
        return self.name
    
class UserMembership(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='membership')
    membership_type = models.ForeignKey(MembershipType, on_delete=models.CASCADE)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()
    remaining_conversations = models.IntegerField()
    remaining_analyses = models.IntegerField()

    def is_active(self):
        return self.end_date >= timezone.now().date()
    
    def __str__(self):
        return f"{self.user.email} - {self.membership_type.name}"
    
    def save(self, *args, **kwargs):
        if not self.end_date:
            self.end_date = timezone.now().date() + timedelta(days=self.membership_type.valid_days)
        super().save(*args, **kwargs)