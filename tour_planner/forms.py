from django import forms
from .models import Itinerary, Destination
from datetime import date
from .choices import TRAVEL_TYPE_CHOICES, WEATHER_CHOICES

class ManualItineraryForm(forms.ModelForm):
    class Meta:
        model = Itinerary
        fields = ['destination', 'start_date', 'end_date', 'budget', 'travel_type', 'preferred_weather']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'min': date.today().strftime('%Y-%m-%d')}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'min': date.today().strftime('%Y-%m-%d')}),
            'travel_type': forms.Select(choices=TRAVEL_TYPE_CHOICES),
            'preferred_weather': forms.Select(choices=WEATHER_CHOICES),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        
        if start_date and end_date:
            if start_date > end_date:
                raise forms.ValidationError("End date should be after start date.")
            
            if (end_date - start_date).days > 30:
                raise forms.ValidationError("Trip duration cannot exceed 30 days.")
        
        return cleaned_data

class AIRecommendationForm(forms.ModelForm):
    class Meta:
        model = Itinerary
        fields = ['start_date', 'end_date', 'budget', 'travel_type', 'preferred_weather']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'min': date.today().strftime('%Y-%m-%d')}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'min': date.today().strftime('%Y-%m-%d')}),
            'travel_type': forms.Select(choices=TRAVEL_TYPE_CHOICES),
            'preferred_weather': forms.Select(choices=WEATHER_CHOICES),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        
        if start_date and end_date:
            if start_date > end_date:
                raise forms.ValidationError("End date should be after start date.")
            
            if (end_date - start_date).days > 30:
                raise forms.ValidationError("Trip duration cannot exceed 30 days.")
        
        return cleaned_data