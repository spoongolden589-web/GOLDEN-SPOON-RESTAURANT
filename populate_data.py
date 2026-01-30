"""
Script to populate the database with sample menu items
Run this with: python manage.py shell < populate_data.py
"""

from main.models import MenuItem

# Sample menu items
sample_items = [
    {
        'name': 'Margherita Pizza',
        'description': 'Classic Italian pizza with fresh mozzarella, tomato sauce, and basil',
        'category': 'main',
        'price': '12.99',
        'ingredients': 'Tomato sauce, Mozzarella cheese, Fresh basil, Olive oil',
        'allergens': 'Gluten, Dairy',
        'is_available': True
    },
    {
        'name': 'Caesar Salad',
        'description': 'Crisp romaine lettuce with Caesar dressing, croutons, and parmesan',
        'category': 'starter',
        'price': '8.99',
        'ingredients': 'Romaine lettuce, Caesar dressing, Croutons, Parmesan cheese',
        'allergens': 'Gluten, Dairy, Eggs, Fish (anchovies)',
        'is_available': True
    },
    {
        'name': 'Spaghetti Carbonara',
        'description': 'Traditional Roman pasta with eggs, pecorino cheese, guanciale, and black pepper',
        'category': 'main',
        'price': '14.99',
        'ingredients': 'Spaghetti, Eggs, Pecorino cheese, Guanciale, Black pepper',
        'allergens': 'Gluten, Dairy, Eggs',
        'is_available': True
    },
    {
        'name': 'Tiramisu',
        'description': 'Classic Italian dessert with coffee-soaked ladyfingers and mascarpone cream',
        'category': 'dessert',
        'price': '6.99',
        'ingredients': 'Ladyfingers, Espresso, Mascarpone, Eggs, Cocoa powder',
        'allergens': 'Gluten, Dairy, Eggs',
        'is_available': True
    },
    {
        'name': 'Bruschetta',
        'description': 'Toasted bread topped with fresh tomatoes, garlic, basil, and olive oil',
        'category': 'starter',
        'price': '7.99',
        'ingredients': 'Bread, Tomatoes, Garlic, Basil, Olive oil',
        'allergens': 'Gluten',
        'is_available': True
    },
    {
        'name': 'Grilled Salmon',
        'description': 'Fresh Atlantic salmon grilled to perfection with lemon butter sauce',
        'category': 'main',
        'price': '18.99',
        'ingredients': 'Salmon, Lemon, Butter, Herbs',
        'allergens': 'Fish, Dairy',
        'is_available': True
    },
    {
        'name': 'Chocolate Lava Cake',
        'description': 'Warm chocolate cake with a molten center, served with vanilla ice cream',
        'category': 'dessert',
        'price': '7.99',
        'ingredients': 'Chocolate, Eggs, Butter, Flour, Sugar',
        'allergens': 'Gluten, Dairy, Eggs',
        'is_available': True
    },
    {
        'name': 'Fresh Orange Juice',
        'description': 'Freshly squeezed orange juice',
        'category': 'drink',
        'price': '3.99',
        'ingredients': 'Fresh oranges',
        'allergens': 'None',
        'is_available': True
    },
    {
        'name': 'Cappuccino',
        'description': 'Espresso with steamed milk and foam',
        'category': 'drink',
        'price': '4.50',
        'ingredients': 'Espresso, Milk',
        'allergens': 'Dairy',
        'is_available': True
    },
    {
        'name': 'Chicken Parmesan',
        'description': 'Breaded chicken breast topped with marinara sauce and melted mozzarella',
        'category': 'main',
        'price': '16.99',
        'ingredients': 'Chicken, Breadcrumbs, Marinara sauce, Mozzarella, Parmesan',
        'allergens': 'Gluten, Dairy',
        'is_available': True
    }
]

# Create menu items
print("Creating sample menu items...")
for item_data in sample_items:
    item, created = MenuItem.objects.get_or_create(
        name=item_data['name'],
        defaults=item_data
    )
    if created:
        print(f"✓ Created: {item.name}")
    else:
        print(f"- Already exists: {item.name}")

print(f"\nTotal menu items in database: {MenuItem.objects.count()}")
print("Done!")
