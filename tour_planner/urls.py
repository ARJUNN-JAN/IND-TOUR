from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('planner/', views.PlannerSelectionView.as_view(), name='planner_selection'),
    path('planner/manual/', views.ManualPlannerView.as_view(), name='manual_planner'),
    path('planner/ai/', views.AIRecommendationView.as_view(), name='ai_recommendation'),
    path('itinerary/<int:pk>/', views.ItineraryDetailView.as_view(), name='itinerary_detail'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
]