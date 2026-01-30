import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'restaurant_core.settings')
django.setup()

from main.models import MenuItem

def update_menu_images():
    """Update menu items with their corresponding images"""
    
    # Mapping of menu item names to image file names
    image_mappings = {
        'Truffle Arancini': 'Truffle Arancini.jfif',
        'Bruschetta': 'Bruschetta.jfif',
        'Caesar Salad': 'caesar salad.jfif',
        'Crispy Calamari': 'crispy calamari.jfif',
        
        'Margherita Pizza': 'margherita pizza.jfif',
        'Spaghetti Carbonara': 'Spaghetti Carbonara.jfif',
        'Grilled Salmon': 'Grilled Salmon.jfif',
        'Chicken Parmesan': 'Chicken Parmesan.jfif',
        
        'Tiramisu': 'Tiramisu.jfif',
        'Chocolate Lava Cake': 'Chocolate Lava Cake.jfif',
        'Classic Crème Brûlée': 'classic cream brucee.jfif',
        'CLASSIC CREME BRULEE': 'classic cream brucee.jfif',
        'ZESTY LEMON TART': 'LEMON ZESTY TART.jfif',
        
        'Cappuccino': 'Cappuccino.jfif',
        'ESPRESSO MARTINI': 'Espresso martini.jfif',
        'Espresso Martini': 'Espresso martini.jfif',
        'CUCUMBER MINT': 'cucumber mint refresher.jfif',
        'Fresh Orange Juice': 'ORANGE JUICE.jfif',
    }
    
    updated_count = 0
    not_found_count = 0
    
    print("Starting image update process...\n")
    
    for item_name, image_file in image_mappings.items():
        try:
            # Find the menu item
            menu_item = MenuItem.objects.get(name=item_name)
            
            # Update the image path
            image_path = f'menu_items/{image_file}'
            menu_item.image = image_path
            menu_item.save()
            
            print(f"✓ Updated: {item_name} -> {image_file}")
            updated_count += 1
            
        except MenuItem.DoesNotExist:
            print(f"✗ Not found: {item_name}")
            not_found_count += 1
        except Exception as e:
            print(f"✗ Error updating {item_name}: {str(e)}")
            not_found_count += 1
    
    print(f"\n{'='*60}")
    print(f"Update Summary:")
    print(f"  Successfully updated: {updated_count}")
    print(f"  Not found/Error: {not_found_count}")
    print(f"{'='*60}\n")
    
    # Display all menu items with their image status
    print("Current Menu Items Status:")
    print(f"{'='*60}")
    for item in MenuItem.objects.all().order_by('category', 'name'):
        image_status = "✓ Has image" if item.image else "✗ No image"
        print(f"{item.name:30} [{item.get_category_display():12}] {image_status}")
        if item.image:
            print(f"  -> {item.image}")

if __name__ == '__main__':
    update_menu_images()
