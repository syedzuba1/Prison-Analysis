from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings


class Prediction1(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to the user
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    age_group = models.CharField(max_length=20)
    prediction = models.CharField(max_length=20)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prediction1 by {self.user.username} at {self.date_created}"


class Prediction2(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to the user
    total_education_facilities = models.FloatField()
    escapee_rate = models.FloatField()
    mental_illness_rate = models.FloatField()
    predicted_escapees = models.FloatField()
    predicted_mental_illness = models.FloatField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prediction2 by {self.user.username} at {self.date_created}"


class Prediction3(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to the user
    state = models.CharField(max_length=100)
    crime_type = models.CharField(max_length=100)
    predicted_status = models.CharField(max_length=20)
    confidence = models.FloatField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prediction3 by {self.user.username} at {self.date_created}"


class Prediction4(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to the user
    state_ut = models.CharField(max_length=100)
    year = models.IntegerField()
    num_years = models.IntegerField()
    predicted_budget = models.FloatField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Prediction4 by {self.user.username} at {self.date_created}"


class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    age = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"UserProfile for {self.user.username}"


@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        # Create the profile only if it doesn't exist
        UserProfile.objects.get_or_create(user=instance)
