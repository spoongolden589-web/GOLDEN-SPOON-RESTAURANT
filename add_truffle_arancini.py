import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'restaurant_core.settings')
django.setup()

from main.models import MenuItem

# Create the new starter
starter_data = {
    'name': 'TRUFFLE ARANCINI',
    'description': 'Golden-fried Italian rice balls filled with creamy risotto, mozzarella, and aromatic truffle oil, served with a rich tomato sauce.',
    'category': 'starter',
    'price': '10.50',
    'ingredients': 'Arborio Rice, Mozzarella, Parmesan, Truffle Oil, Breadcrumbs, Tomato Sauce, Fresh Herbs',
    'allergens': 'Contains: Gluten, Dairy, Eggs',
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
