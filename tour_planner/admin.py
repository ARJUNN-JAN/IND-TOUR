from django.contrib import admin
from .models import Destination, LocalCuisine, Itinerary, ItineraryDay

admin.site.register(Destination)
admin.site.register(LocalCuisine)
admin.site.register(Itinerary)
admin.site.register(ItineraryDay)
