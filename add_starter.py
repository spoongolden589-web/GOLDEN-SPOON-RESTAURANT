import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'restaurant_core.settings')
django.setup()

from main.models import MenuItem

# Create the new starter
starter_data = {
    'name': 'CRISPY CALAMARI',
    'description': 'Tender squid rings lightly battered and fried to golden perfection, served with a zesty lemon aioli and fresh herbs.',
    'category': 'starter',
    'price': '11.50',
    'ingredients': 'Squid, Flour, Cornstarch, Garlic, Lemon, Aioli, Fresh Parsley',
    'allergens': 'Contains: Seafood, Gluten, Eggs',
    'is_available': True
}

starter, created = MenuItem.objects.get_or_create(
    name=starter_data['name'],
    defaults=starter_data
)

if created:
    print(f"✓ Added: {starter.name}")
    print(f"  Category: {starter.get_category_display()}")
    print(f"  Price: £{starter.price}")
else:
    print(f"- Already exists: {starter.name}")
    print(f"  This item is already in your menu's starter section")
