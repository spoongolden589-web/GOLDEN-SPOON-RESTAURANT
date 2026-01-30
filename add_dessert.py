import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'restaurant_core.settings')
django.setup()

from main.models import MenuItem

# Create the new dessert
dessert_data = {
    'name': 'CLASSIC CREME BRULEE',
    'description': 'A timeless French dessert featuring silky smooth vanilla custard with a perfectly caramelized sugar crust that shatters with each spoonful.',
    'category': 'dessert',
    'price': '7.50',
    'ingredients': 'Heavy Cream, Egg Yolks, Vanilla Bean, Sugar, Caramel',
    'allergens': 'Contains: Eggs, Dairy',
    'is_available': True
}

dessert, created = MenuItem.objects.get_or_create(
    name=dessert_data['name'],
    defaults=dessert_data
)

if created:
    print(f"✓ Added: {dessert.name}")
    print(f"  Category: {dessert.get_category_display()}")
    print(f"  Price: £{dessert.price}")
else:
    print(f"- Already exists: {dessert.name}")
