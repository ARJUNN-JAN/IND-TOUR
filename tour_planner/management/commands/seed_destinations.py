from django.core.management.base import BaseCommand
from tour_planner.models import Destination, LocalCuisine

class Command(BaseCommand):
    help = 'Seeds the database with initial destinations and cuisines'

    def handle(self, *args, **kwargs):
        # Clear existing data
        Destination.objects.all().delete()
        LocalCuisine.objects.all().delete()
        destinations = [
            {
                'name': 'Jaipur',
                'description': 'Known as the Pink City, Jaipur is famous for its stunning architecture and royal heritage.',
                'best_season': 'winter',
                'budget_range_min': 10000,
                'budget_range_max': 50000,
                'suitable_for': 'family friends couple',
                'cuisines': [
                    {'name': 'Dal Baati Churma', 'description': 'Traditional Rajasthani dish with lentils and baked wheat balls'},
                    {'name': 'Ghewar', 'description': 'Sweet disc-shaped dessert made with flour and soaked in sugar syrup'},
                    {'name': 'Laal Maas', 'description': 'Spicy meat curry cooked with red chilies'}
                ]
            },
            {
                'name': 'Varanasi',
                'description': 'One of the oldest continuously inhabited cities in the world, known for its spiritual significance.',
                'best_season': 'winter',
                'budget_range_min': 5000,
                'budget_range_max': 30000,
                'suitable_for': 'spiritual solo',
                'cuisines': [
                    {'name': 'Banarasi Paan', 'description': 'Betel leaf filled with areca nut and other flavorings'},
                    {'name': 'Malaiyo', 'description': 'Seasonal dessert made with milk foam, saffron, and nuts'},
                    {'name': 'Kachori Sabzi', 'description': 'Fried pastry filled with spiced lentils, served with potato curry'}
                ]
            },
            {
                'name': 'Goa',
                'description': 'Famous for its beaches, nightlife, and Portuguese-influenced architecture.',
                'best_season': 'winter',
                'budget_range_min': 15000,
                'budget_range_max': 70000,
                'suitable_for': 'friends couple solo',
                'cuisines': [
                    {'name': 'Fish Curry Rice', 'description': 'Goan staple with coconut-based curry and local fish'},
                    {'name': 'Vindaloo', 'description': 'Spicy curry made with meat, vinegar, and Kashmiri chilies'},
                    {'name': 'Bebinca', 'description': 'Traditional layered pudding dessert'}
                ]
            },
            {
                'name': 'Rishikesh',
                'description': 'Yoga capital of the world, situated in the foothills of the Himalayas along the Ganges River.',
                'best_season': 'spring autumn',
                'budget_range_min': 8000,
                'budget_range_max': 40000,
                'suitable_for': 'spiritual solo',
                'cuisines': [
                    {'name': 'Chole Bhature', 'description': 'Spicy chickpea curry served with fried bread'},
                    {'name': 'Aloo Puri', 'description': 'Potato curry served with deep-fried bread'},
                    {'name': 'Fruit Lassi', 'description': 'Yogurt-based drink blended with fresh fruits'}
                ]
            },
            {
                'name': 'Darjeeling',
                'description': 'Hill station famous for its tea plantations and views of the Himalayas.',
                'best_season': 'spring summer',
                'budget_range_min': 12000,
                'budget_range_max': 45000,
                'suitable_for': 'family couple',
                'cuisines': [
                    {'name': 'Momos', 'description': 'Steamed dumplings filled with meat or vegetables'},
                    {'name': 'Thukpa', 'description': 'Noodle soup with vegetables and meat'},
                    {'name': 'Sel Roti', 'description': 'Ring-shaped rice bread/doughnut'}
                ]
            },
            {
                'name': 'Kerala Backwaters',
                'description': 'Network of lakes, canals, and rivers surrounded by lush greenery.',
                'best_season': 'winter',
                'budget_range_min': 15000,
                'budget_range_max': 60000,
                'suitable_for': 'couple family',
                'cuisines': [
                    {'name': 'Appam with Stew', 'description': 'Fermented rice pancake with coconut milk stew'},
                    {'name': 'Kerala Fish Curry', 'description': 'Spicy fish curry with coconut and tamarind'},
                    {'name': 'Puttu and Kadala Curry', 'description': 'Steamed rice cake with black chickpea curry'}
                ]
            },
            {
                'name': 'Ladakh',
                'description': 'High-altitude desert known for its stunning landscapes and Buddhist monasteries.',
                'best_season': 'summer',
                'budget_range_min': 20000,
                'budget_range_max': 80000,
                'suitable_for': 'adventure solo friends',
                'cuisines': [
                    {'name': 'Thukpa', 'description': 'Noodle soup with vegetables and meat'},
                    {'name': 'Skyu', 'description': 'Pasta dish with vegetables and meat'},
                    {'name': 'Butter Tea', 'description': 'Traditional tea made with yak butter and salt'}
                ]
            },
            {
                'name': 'Agra',
                'description': 'Home to the iconic Taj Mahal and other Mughal-era architecture.',
                'best_season': 'winter autumn',
                'budget_range_min': 10000,
                'budget_range_max': 40000,
                'suitable_for': 'family couple friends',
                'cuisines': [
                    {'name': 'Petha', 'description': 'Soft candy made from ash gourd/winter melon'},
                    {'name': 'Bedai', 'description': 'Fried bread served with spicy potato curry'},
                    {'name': 'Mughlai Cuisine', 'description': 'Rich, creamy curries and kebabs influenced by Mughal cooking'}
                ]
            },
            {
                'name': 'Udaipur',
                'description': 'City of lakes with beautiful palaces and a romantic atmosphere.',
                'best_season': 'winter autumn',
                'budget_range_min': 12000,
                'budget_range_max': 55000,
                'suitable_for': 'couple family',
                'cuisines': [
                    {'name': 'Dal Baati Churma', 'description': 'Traditional Rajasthani dish with lentils and baked wheat balls'},
                    {'name': 'Gatte ki Sabzi', 'description': 'Curry made with gram flour dumplings'},
                    {'name': 'Mawa Kachori', 'description': 'Sweet kachori filled with mawa (milk solids) and dry fruits'}
                ]
            },
            {
                'name': 'Andaman Islands',
                'description': 'Archipelago known for pristine beaches, coral reefs, and marine life.',
                'best_season': 'winter',
                'budget_range_min': 25000,
                'budget_range_max': 90000,
                'suitable_for': 'couple friends adventure',
                'cuisines': [
                    {'name': 'Fish Curry', 'description': 'Fresh seafood in coconut-based curry'},
                    {'name': 'Grilled Lobster', 'description': 'Fresh lobster grilled with local spices'},
                    {'name': 'Coconut Prawn Curry', 'description': 'Prawns cooked in coconut milk with spices'}
                ]
            }
        ]
        
        # Add destinations and cuisines to database
        for dest_data in destinations:
            cuisines = dest_data.pop('cuisines')
            destination = Destination.objects.create(**dest_data)
            
            for cuisine_data in cuisines:
                LocalCuisine.objects.create(destination=destination, **cuisine_data)
        
        self.stdout.write(self.style.SUCCESS(f'Successfully added {len(destinations)} destinations with their cuisines'))