import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'restaurant_core.settings')
django.setup()

from main.models import MenuItem

# Update ZESTY LEMON TART from drink to dessert
try:
    item = MenuItem.objects.get(name='ZESTY LEMON TART')
    item.category = 'dessert'
    item.description = 'A classic French-style lemon tart with a buttery shortcrust pastry, silky smooth lemon custard filling, and a perfectly caramelized top.'
    item.ingredients = 'Shortcrust Pastry, Fresh Lemons, Eggs, Sugar, Cream, Butter'
    item.allergens = 'Contains: Gluten, Eggs, Dairy'
    item.price = '8.50'
    item.save()
    print(f"✓ Successfully moved '{item.name}' from drinks to desserts section")
    print(f"  Category: {item.get_category_display()}")
    print(f"  Price: £{item.price}")
except MenuItem.DoesNotExist:
    print("✗ Item 'ZESTY LEMON TART' not found in database")
