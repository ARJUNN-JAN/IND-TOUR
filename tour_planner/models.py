from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Destination(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    best_season = models.CharField(max_length=50)
    budget_range_min = models.IntegerField()
    budget_range_max = models.IntegerField()
    suitable_for = models.CharField(max_length=100)  # solo, spiritual, family, etc.
    
    def __str__(self):
        return self.name

class LocalCuisine(models.Model):
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, related_name='cuisines')
    name = models.CharField(max_length=100)
    description = models.TextField()
    
    def __str__(self):
        return f"{self.name} - {self.destination.name}"

class Itinerary(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    destination = models.ForeignKey(Destination, on_delete=models.CASCADE, null=True, blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    budget = models.IntegerField()
    travel_type = models.CharField(max_length=50)  # solo, spiritual, family, etc.
    preferred_weather = models.CharField(max_length=50)  # summer, winter, etc.
    is_ai_recommended = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        destination_name = self.destination.name if self.destination else "AI Recommended"
        return f"{destination_name} - {self.start_date} to {self.end_date}"

class ItineraryDay(models.Model):
    itinerary = models.ForeignKey(Itinerary, on_delete=models.CASCADE, related_name='days')
    day_number = models.IntegerField()
    activities = models.TextField()
    accommodation = models.CharField(max_length=100)
    meals = models.TextField()
    
    def __str__(self):
        return f"Day {self.day_number} - {self.itinerary}"
