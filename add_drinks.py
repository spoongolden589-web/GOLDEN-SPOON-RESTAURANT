import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'restaurant_core.settings')
django.setup()

from main.models import MenuItem

# Create the new starter
starters = [
    {
        'name': 'CRISPY CALAMARI',
        'description': 'Tender squid rings lightly battered and fried to golden perfection, served with a zesty lemon aioli and fresh herbs.',
        'category': 'starter',
        'price': '11.50',
        'ingredients': 'Squid, Flour, Cornstarch, Garlic, Lemon, Aioli, Fresh Parsley',
        'allergens': 'Contains: Seafood, Gluten, Eggs',
        'is_available': True
    }
]

# Create the new drinks
drinks = [
    {
        'name': 'ESPRESSO MARTINI',
        'description': 'A sophisticated blend of premium vodka, freshly brewed espresso, and coffee liqueur, shaken to perfection for a velvety smooth finish.',
        'category': 'drink',
        'price': '12.50',
        'ingredients': 'Vodka, Espresso, Coffee Liqueur, Sugar Syrup',
        'allergens': '',
        'is_available': True
    },
    {
        'name': 'CUCUMBER MINT',
        'description': 'A refreshing combination of crisp cucumber, fresh mint leaves, and sparkling water, perfectly balanced with a hint of lime.',
        'category': 'drink',
        'price': '7.50',
        'ingredients': 'Fresh Cucumber, Mint Leaves, Lime Juice, Sparkling Water, Simple Syrup',
        'allergens': '',
        'is_available': True
    },
    {
        'name': 'ZESTY LEMON TART',
        'description': 'A bright and tangy lemon-infused cocktail with a smooth vanilla finish, garnished with crystallized lemon zest.',
        'category': 'drink',
        'price': '9.50',
        'ingredients': 'Lemon Juice, Vodka, Vanilla Syrup, Triple Sec, Lemon Zest',
        'allergens': '',
        'is_available': True
    }
]

print("Adding starters to menu...")
for starter_data in starters:
    starter, created = MenuItem.objects.get_or_create(
        name=starter_data['name'],
        defaults=starter_data
    )
    if created:
        print(f"✓ Added: {starter.name}")
    else:
        print(f"- Already exists: {starter.name}")

print("\nAdding drinks to menu...")
for drink_data in drinks:
    drink, created = MenuItem.objects.get_or_create(
        name=drink_data['name'],
        defaults=drink_data
    )
    if created:
        print(f"✓ Added: {drink.name}")
    else:
        print(f"- Already exists: {drink.name}")

print("\nAll items successfully added to the menu!")
