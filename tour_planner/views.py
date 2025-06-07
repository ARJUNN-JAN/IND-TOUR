from django.shortcuts import render, redirect
from django.views import View
from .forms import ManualItineraryForm, AIRecommendationForm
from .models import Destination, Itinerary, ItineraryDay, LocalCuisine
from datetime import datetime, timedelta
import random
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from django.contrib.auth.mixins import LoginRequiredMixin

class ProfileView(LoginRequiredMixin, View):
    def get(self, request):
        return render(request, 'tour_planner/profile.html')

class HomeView(View):
    def get(self, request):
        return render(request, 'tour_planner/home.html')

class PlannerSelectionView(View):
    def get(self, request):
        return render(request, 'tour_planner/planner_selection.html')

class ManualPlannerView(View):
    def get(self, request):
        form = ManualItineraryForm()
        return render(request, 'tour_planner/manual_planner.html', {'form': form})
    
    def post(self, request):
        form = ManualItineraryForm(request.POST)
        if form.is_valid():
            itinerary = form.save(commit=False)
            if request.user.is_authenticated:
                itinerary.user = request.user
            itinerary.is_ai_recommended = False
            itinerary.save()
            
            # Generate itinerary days
            self.generate_itinerary_days(itinerary)
            
            return redirect('itinerary_detail', pk=itinerary.pk)
        return render(request, 'tour_planner/manual_planner.html', {'form': form})
    
    def generate_itinerary_days(self, itinerary):
        # Calculate number of days
        delta = itinerary.end_date - itinerary.start_date
        num_days = delta.days + 1
        
        # Get local cuisines
        local_cuisines = list(LocalCuisine.objects.filter(destination=itinerary.destination))
        
        # Generate itinerary for each day
        for day in range(1, num_days + 1):
            activities = self.generate_activities(itinerary.destination, day, num_days)
            accommodation = self.generate_accommodation(itinerary.destination)
            meals = self.generate_meals(local_cuisines)
            
            ItineraryDay.objects.create(
                itinerary=itinerary,
                day_number=day,
                activities=activities,
                accommodation=accommodation,
                meals=meals
            )
    
    def generate_activities(self, destination, day, total_days):
        # This is a simplified version. In a real app, you'd have a database of activities
        activities = [
            f"Morning: Visit {destination.name}'s famous landmarks",
            f"Afternoon: Explore local markets and shops",
            f"Evening: Enjoy cultural performances"
        ]
        
        if day == 1:
            activities[0] = "Morning: Arrive and check-in to accommodation"
        
        if day == total_days:
            activities[2] = "Evening: Pack and prepare for departure tomorrow"
            
        return "\n".join(activities)
    
    def generate_accommodation(self, destination):
        accommodations = [
            f"Hotel in central {destination.name}",
            f"Guesthouse near {destination.name} market",
            f"Resort with view of {destination.name} landscape"
        ]
        return random.choice(accommodations)
    
    def generate_meals(self, local_cuisines):
        if local_cuisines:
            cuisines = random.sample(local_cuisines, min(3, len(local_cuisines)))
            return "Recommended local dishes:\n" + "\n".join([cuisine.name for cuisine in cuisines])
        else:
            return "Explore local restaurants for authentic cuisine"

class AIRecommendationView(View):
    def get(self, request):
        form = AIRecommendationForm()
        return render(request, 'tour_planner/ai_recommendation.html', {'form': form})
    
    def post(self, request):
        form = AIRecommendationForm(request.POST)
        if form.is_valid():
            itinerary = form.save(commit=False)
            if request.user.is_authenticated:
                itinerary.user = request.user
            itinerary.is_ai_recommended = True
            
            # AI recommendation logic
            recommended_destination = self.recommend_destination(
                budget=itinerary.budget,
                travel_type=itinerary.travel_type,
                preferred_weather=itinerary.preferred_weather,
                start_date=itinerary.start_date
            )
            
            itinerary.destination = recommended_destination
            itinerary.save()
            
            # Generate itinerary days
            self.generate_itinerary_days(itinerary)
            
            return redirect('itinerary_detail', pk=itinerary.pk)
        return render(request, 'tour_planner/ai_recommendation.html', {'form': form})
    
    def recommend_destination(self, budget, travel_type, preferred_weather, start_date):
        # Get all destinations
        destinations = Destination.objects.all()
        
        if not destinations:
            # If no destinations in database, return None or create a default
            return None
        
        # Filter by budget
        budget_destinations = [d for d in destinations if d.budget_range_min <= budget <= d.budget_range_max]
        
        if not budget_destinations:
            # If no destinations match budget, use all destinations
            budget_destinations = destinations
        
        # Create feature vectors for destinations
        features = []
        for dest in budget_destinations:
            # Create a feature string combining relevant attributes
            feature = f"{dest.suitable_for} {dest.best_season}"
            features.append(feature)
        
        # Create feature vector for user preferences
        user_feature = f"{travel_type} {preferred_weather}"
        
        # Use TF-IDF to convert text to vectors
        vectorizer = TfidfVectorizer()
        try:
            # Add user feature to the list for vectorization
            all_features = features + [user_feature]
            tfidf_matrix = vectorizer.fit_transform(all_features)
            
            # Calculate similarity between user preferences and each destination
            user_vector = tfidf_matrix[-1]  # Last vector is the user's
            destination_vectors = tfidf_matrix[:-1]  # All except the last are destinations
            
            similarities = cosine_similarity(user_vector, destination_vectors)[0]
            
            # Get the index of the most similar destination
            best_match_idx = np.argmax(similarities)
            
            return budget_destinations[best_match_idx]
        except:
            # Fallback if vectorization fails
            return random.choice(budget_destinations)
    
    def generate_itinerary_days(self, itinerary):
        # Similar to the manual planner's method
        delta = itinerary.end_date - itinerary.start_date
        num_days = delta.days + 1
        
        local_cuisines = list(LocalCuisine.objects.filter(destination=itinerary.destination))
        
        for day in range(1, num_days + 1):
            activities = self.generate_activities(itinerary.destination, day, num_days, itinerary.travel_type)
            accommodation = self.generate_accommodation(itinerary.destination, itinerary.budget)
            meals = self.generate_meals(local_cuisines)
            
            ItineraryDay.objects.create(
                itinerary=itinerary,
                day_number=day,
                activities=activities,
                accommodation=accommodation,
                meals=meals
            )
    
    def generate_activities(self, destination, day, total_days, travel_type):
        # Customize activities based on travel type
        activities = []
        
        if travel_type == 'solo':
            activities = [
                f"Morning: Explore {destination.name} at your own pace",
                f"Afternoon: Join a group tour to meet fellow travelers",
                f"Evening: Relax at a local café or restaurant"
            ]
        elif travel_type == 'spiritual':
            activities = [
                f"Morning: Visit temples and spiritual sites in {destination.name}",
                f"Afternoon: Meditation session at a peaceful location",
                f"Evening: Attend spiritual discourse or ritual"
            ]
        else:  # family or default
            activities = [
                f"Morning: Visit family-friendly attractions in {destination.name}",
                f"Afternoon: Leisure activities suitable for all ages",
                f"Evening: Enjoy cultural performances or dinner together"
            ]
        
        if day == 1:
            activities[0] = "Morning: Arrive and check-in to accommodation"
        
        if day == total_days:
            activities[2] = "Evening: Pack and prepare for departure tomorrow"
            
        return "\n".join(activities)
    
    def generate_accommodation(self, destination, budget):
        # Adjust accommodation based on budget
        if budget > 50000:  # High budget
            accommodations = [
                f"Luxury hotel in {destination.name}",
                f"Premium resort with all amenities",
                f"Boutique hotel with personalized service"
            ]
        elif budget > 20000:  # Medium budget
            accommodations = [
                f"Comfortable hotel in {destination.name}",
                f"Well-rated guesthouse with good facilities",
                f"Service apartment with kitchen facilities"
            ]
        else:  # Budget option
            accommodations = [
                f"Budget-friendly hostel in {destination.name}",
                f"Affordable guesthouse with basic amenities",
                f"Homestay experience with locals"
            ]
        return random.choice(accommodations)
    
    def generate_meals(self, local_cuisines):
        if local_cuisines:
            cuisines = random.sample(local_cuisines, min(3, len(local_cuisines)))
            return "Recommended local dishes:\n" + "\n".join([f"{cuisine.name}: {cuisine.description}" for cuisine in cuisines])
        else:
            return "Explore local restaurants for authentic cuisine"

class ItineraryDetailView(View):
    def get(self, request, pk):
        try:
            itinerary = Itinerary.objects.get(pk=pk)
            days = ItineraryDay.objects.filter(itinerary=itinerary).order_by('day_number')
            
            # Generate weather information based on destination and season
            weather_info = self.get_weather_info(itinerary.destination, itinerary.start_date)
            
            context = {
                'itinerary': itinerary,
                'days': days,
                'weather_info': weather_info
            }
            
            return render(request, 'tour_planner/itinerary_detail.html', context)
        except Itinerary.DoesNotExist:
            return redirect('home')
    
    def get_weather_info(self, destination, start_date):
        # This is a simplified version. In a real app, you might use a weather API
        month = start_date.month
        
        if destination.best_season == 'summer' and month in [4, 5, 6]:
            return f"Perfect time to visit {destination.name}! Expect warm, sunny days."
        elif destination.best_season == 'winter' and month in [11, 12, 1, 2]:
            return f"Great time to visit {destination.name}! Expect cool, pleasant weather."
        elif destination.best_season == 'monsoon' and month in [7, 8, 9]:
            return f"It's monsoon season in {destination.name}. Pack an umbrella and enjoy the lush greenery!"
        elif destination.best_season == 'spring' and month in [2, 3, 4]:
            return f"Spring is a beautiful time in {destination.name} with moderate temperatures."
        elif destination.best_season == 'autumn' and month in [9, 10, 11]:
            return f"Autumn in {destination.name} offers pleasant weather and fewer crowds."
        else:
            return f"Note: You're not visiting {destination.name} during its peak season. Weather may vary."
