from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
from django.db.models import Q, Sum
from django.utils import timezone
from decimal import Decimal
from datetime import datetime, timedelta
import json

from .models import MenuItem, Order, OrderItem, Reservation, UserProfile
from .web3forms import send_order_confirmation, send_reservation_confirmation, send_admin_notification


# ==================== PUBLIC PAGES ====================

def home(request):
    """Homepage with featured items"""
    featured_items = MenuItem.objects.filter(is_available=True)[:6]
    menu_items = MenuItem.objects.filter(is_available=True)[:8]  # For the Webfoutend section
    context = {
        'featured_items': featured_items,
        'menu_items': menu_items,
    }
    return render(request, 'main/home.html', context)


def about(request):
    """About page with restaurant information"""
    return render(request, 'main/about.html')


def locations(request):
    """Locations page with address and opening hours"""
    return render(request, 'main/locations.html')


def menu(request):
    """Display all menu items by category"""
    category = request.GET.get('category', '')
    
    if category:
        items = MenuItem.objects.filter(category=category, is_available=True)
    else:
        items = MenuItem.objects.filter(is_available=True)
    
    categories = MenuItem.CATEGORY_CHOICES
    
    context = {
        'items': items,
        'categories': categories,
        'selected_category': category,
    }
    return render(request, 'main/menu.html', context)


def menu_detail(request, item_id):
    """Display detailed information about a menu item"""
    item = get_object_or_404(MenuItem, id=item_id)
    context = {
        'item': item,
    }
    return render(request, 'main/menu_detail.html', context)


# ==================== AUTHENTICATION ====================

def signup(request):
    """User registration"""
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        phone = request.POST.get('phone', '')
        address = request.POST.get('address', '')
        
        # Validation
        if password != password2:
            messages.error(request, 'Passwords do not match!')
            return render(request, 'main/signup.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists!')
            return render(request, 'main/signup.html')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered!')
            return render(request, 'main/signup.html')
        
        # Create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        
        # Create user profile
        UserProfile.objects.create(
            user=user,
            phone=phone,
            address=address
        )
        
        # Send welcome email
        try:
            send_mail(
                'Welcome to Our Restaurant!',
                f'Hi {username},\n\nThank you for signing up! Your account has been created successfully.',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=True,
            )
        except:
            pass
        
        messages.success(request, 'Account created successfully! Please log in.')
        return redirect('main:login')
    
    return render(request, 'main/signup.html')


def user_login(request):
    """User login"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            next_url = request.GET.get('next', 'main:home')
            return redirect(next_url)
        else:
            messages.error(request, 'Invalid username or password!')
    
    return render(request, 'main/login.html')


def user_logout(request):
    """User logout"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('main:home')


@login_required
def profile(request):
    """User profile page"""
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        # Update profile
        request.user.email = request.POST.get('email', request.user.email)
        request.user.save()
        
        profile.phone = request.POST.get('phone', '')
        profile.address = request.POST.get('address', '')
        profile.save()
        
        messages.success(request, 'Profile updated successfully!')
        return redirect('main:profile')
    
    # Get user's recent orders
    recent_orders = Order.objects.filter(user=request.user)[:5]
    
    context = {
        'profile': profile,
        'recent_orders': recent_orders,
    }
    return render(request, 'main/profile.html', context)


# ==================== BASKET / CART ====================

def get_basket(request):
    """Get basket from session"""
    basket = request.session.get('basket', {})
    return basket


def save_basket(request, basket):
    """Save basket to session"""
    request.session['basket'] = basket
    request.session.modified = True


def basket(request):
    """View basket"""
    basket = get_basket(request)
    basket_items = []
    total = Decimal('0.00')
    
    for item_id, quantity in basket.items():
        try:
            menu_item = MenuItem.objects.get(id=int(item_id))
            subtotal = menu_item.price * quantity
            basket_items.append({
                'item': menu_item,
                'quantity': quantity,
                'subtotal': subtotal,
            })
            total += subtotal
        except MenuItem.DoesNotExist:
            pass
    
    context = {
        'basket_items': basket_items,
        'total': total,
    }
    return render(request, 'main/basket.html', context)


def add_to_basket(request, item_id):
    """Add item to basket"""
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        basket = get_basket(request)
        
        # Verify item exists
        try:
            menu_item = MenuItem.objects.get(id=item_id, is_available=True)
        except MenuItem.DoesNotExist:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'error': 'Item not found or not available'
                }, status=404)
            messages.error(request, 'Item not found or not available!')
            return redirect('main:menu')
        
        item_id_str = str(item_id)
        if item_id_str in basket:
            basket[item_id_str] += quantity
        else:
            basket[item_id_str] = quantity
        
        save_basket(request, basket)
        
        # Calculate basket count
        basket_count = sum(basket.values())
        
        # Return JSON for AJAX requests
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': 'Item added to basket!',
                'basket_count': basket_count,
                'item_name': menu_item.name
            })
        
        messages.success(request, 'Item added to basket!')
        return redirect('main:menu')
    
    return redirect('main:menu')


def update_basket(request, item_id):
    """Update quantity in basket"""
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        basket = get_basket(request)
        
        if quantity > 0:
            basket[str(item_id)] = quantity
        else:
            basket.pop(str(item_id), None)
        
        save_basket(request, basket)
        messages.success(request, 'Basket updated!')
        
        # Handle AJAX requests
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            # Calculate new totals
            basket_items = []
            total = Decimal('0.00')
            
            for bid, qty in basket.items():
                try:
                    menu_item = MenuItem.objects.get(id=int(bid))
                    item_total = menu_item.price * qty
                    basket_items.append({
                        'item_id': bid,
                        'subtotal': float(item_total)
                    })
                    total += item_total
                except MenuItem.DoesNotExist:
                    pass
            
            return JsonResponse({
                'success': True,
                'total': float(total),
                'item_id': item_id,
                'quantity': quantity,
                'subtotal': float(MenuItem.objects.get(id=item_id).price * quantity) if quantity > 0 else 0
            })
    
    return redirect('main:basket')


def remove_from_basket(request, item_id):
    """Remove item from basket"""
    basket = get_basket(request)
    basket.pop(str(item_id), None)
    save_basket(request, basket)
    messages.success(request, 'Item removed from basket!')
    
    # Handle AJAX requests
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Calculate new totals
        total = Decimal('0.00')
        
        for bid, qty in basket.items():
            try:
                menu_item = MenuItem.objects.get(id=int(bid))
                total += menu_item.price * qty
            except MenuItem.DoesNotExist:
                pass
        
        return JsonResponse({
            'success': True,
            'total': float(total),
            'item_id': item_id,
            'basket_empty': len(basket) == 0
        })
    
    return redirect('main:basket')


# ==================== CHECKOUT & PAYMENT ====================

def checkout(request):
    """Checkout page"""
    basket = get_basket(request)
    
    if not basket:
        messages.warning(request, 'Your basket is empty!')
        return redirect('main:menu')
    
    # Calculate totals
    basket_items = []
    subtotal = Decimal('0.00')
    
    for item_id, quantity in basket.items():
        try:
            menu_item = MenuItem.objects.get(id=int(item_id))
            item_total = menu_item.price * quantity
            basket_items.append({
                'item': menu_item,
                'quantity': quantity,
                'subtotal': item_total,
            })
            subtotal += item_total
        except MenuItem.DoesNotExist:
            pass
    
    delivery_fee = Decimal('5.00')  # Fixed delivery fee
    
    context = {
        'basket_items': basket_items,
        'subtotal': subtotal,
        'delivery_fee': delivery_fee,
        'total': subtotal + delivery_fee,
    }
    return render(request, 'main/checkout.html', context)


def process_payment(request):
    """Process payment and create order"""
    if request.method == 'POST':
        basket = get_basket(request)
        
        if not basket:
            messages.error(request, 'Your basket is empty!')
            return redirect('main:menu')
        
        # Get form data
        order_type = request.POST.get('order_type')
        delivery_address = request.POST.get('delivery_address', '')
        collection_time = request.POST.get('collection_time', '')
        payment_method = request.POST.get('payment_method', 'card')
        payment_token = request.POST.get('payment_token', 'TEST_TOKEN')
        
        # Get guest information
        guest_name = request.POST.get('guest_name', '')
        guest_email = request.POST.get('guest_email', '')
        guest_phone = request.POST.get('guest_phone', '')
        
        # Calculate totals
        subtotal = Decimal('0.00')
        for item_id, quantity in basket.items():
            try:
                menu_item = MenuItem.objects.get(id=int(item_id))
                subtotal += menu_item.price * quantity
            except MenuItem.DoesNotExist:
                pass
        
        delivery_fee = Decimal('5.00') if order_type == 'delivery' else Decimal('0.00')
        total = subtotal + delivery_fee
        
        # Create order for authenticated or guest user
        order = Order.objects.create(
            user=request.user if request.user.is_authenticated else None,
            order_type=order_type,
            status='paid',
            delivery_address=delivery_address if order_type == 'delivery' else '',
            collection_time=timezone.now() + timedelta(hours=1) if order_type == 'collection' else None,
            subtotal=subtotal,
            delivery_fee=delivery_fee,
            total=total,
            payment_method=payment_method,
            payment_token=payment_token,
            guest_name=guest_name,
            guest_email=guest_email,
            guest_phone=guest_phone
        )
        
        # Create order items
        for item_id, quantity in basket.items():
            try:
                menu_item = MenuItem.objects.get(id=int(item_id))
                OrderItem.objects.create(
                    order=order,
                    menu_item=menu_item,
                    quantity=quantity,
                    price=menu_item.price
                )
            except MenuItem.DoesNotExist:
                pass
        
        # Clear basket
        request.session['basket'] = {}
        request.session.modified = True
        
        # Send confirmation email via Web3Forms
        web3forms_key = getattr(settings, 'WEB3FORMS_ACCESS_KEY', None)
        if web3forms_key:
            try:
                # Send customer confirmation
                send_order_confirmation(web3forms_key, order)
                
                # Send admin notification
                admin_email = getattr(settings, 'ADMIN_EMAIL', 'admin@restaurant.com')
                details = f"""
Order Number: {order.order_number}
Customer: {guest_name if guest_name else (request.user.username if request.user.is_authenticated else 'Unknown')}
Email: {guest_email if guest_email else (request.user.email if request.user.is_authenticated else 'N/A')}
Phone: {guest_phone}
Order Type: {order.get_order_type_display()}
Total: £{order.total}
"""
                send_admin_notification(web3forms_key, admin_email, "Order", details)
            except Exception as e:
                # Log error but don't fail the order
                print(f"Email notification error: {e}")
        
        messages.success(request, 'Order placed successfully!')
        return redirect('main:order_confirmation', order_number=order.order_number)
    
    return redirect('main:checkout')


def order_confirmation(request, order_number):
    """Order confirmation page"""
    order = get_object_or_404(Order, order_number=order_number)
    # Allow access for both authenticated users and guests
    if request.user.is_authenticated and order.user != request.user:
        messages.error(request, 'Access denied!')
        return redirect('main:home')
    context = {
        'order': order,
    }
    return render(request, 'main/order_confirmation.html', context)


# ==================== RESERVATIONS ====================

def make_reservation(request):
    """Make a table reservation"""
    if request.method == 'POST':
        date_str = request.POST.get('date')
        time_str = request.POST.get('time')
        guests = int(request.POST.get('guests'))
        special_requests = request.POST.get('special_requests', '')
        
        # Get guest information
        guest_name = request.POST.get('guest_name', '')
        guest_email = request.POST.get('guest_email', '')
        guest_phone = request.POST.get('guest_phone', '')
        
        # Parse date and time
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
            time = datetime.strptime(time_str, '%H:%M').time()
        except ValueError:
            messages.error(request, 'Invalid date or time format!')
            return render(request, 'main/reservations.html')
        
        # Check if slot is available
        if Reservation.objects.filter(date=date, time=time).exists():
            messages.error(request, 'This time slot is already booked. Please choose another time.')
            return render(request, 'main/reservations.html')
        
        # Create reservation for authenticated or guest user
        reservation = Reservation.objects.create(
            user=request.user if request.user.is_authenticated else None,
            date=date,
            time=time,
            guests=guests,
            special_requests=special_requests,
            status='confirmed',
            guest_name=guest_name,
            guest_email=guest_email,
            guest_phone=guest_phone
        )
        
        # Send confirmation email via Web3Forms
        web3forms_key = getattr(settings, 'WEB3FORMS_ACCESS_KEY', None)
        if web3forms_key:
            try:
                # Send customer confirmation
                send_reservation_confirmation(web3forms_key, reservation)
                
                # Send admin notification
                admin_email = getattr(settings, 'ADMIN_EMAIL', 'admin@restaurant.com')
                details = f"""
Reservation Number: {reservation.reservation_number}
Guest Name: {guest_name if guest_name else (request.user.username if request.user.is_authenticated else 'Unknown')}
Email: {guest_email if guest_email else (request.user.email if request.user.is_authenticated else 'N/A')}
Phone: {guest_phone}
Date: {date}
Time: {time}
Number of Guests: {guests}
Special Requests: {special_requests if special_requests else 'None'}
"""
                send_admin_notification(web3forms_key, admin_email, "Reservation", details)
            except Exception as e:
                # Log error but don't fail the reservation
                print(f"Email notification error: {e}")
        
        messages.success(request, 'Reservation confirmed!')
        return redirect('main:reservation_confirmation', reservation_number=reservation.reservation_number)
    
    return render(request, 'main/reservations.html')


def reservation_confirmation(request, reservation_number):
    """Reservation confirmation page"""
    reservation = get_object_or_404(Reservation, reservation_number=reservation_number)
    # Allow access for both authenticated users and guests
    if request.user.is_authenticated and reservation.user and reservation.user != request.user:
        messages.error(request, 'Access denied!')
        return redirect('main:home')
    context = {
        'reservation': reservation,
    }
    return render(request, 'main/reservation_confirmation.html', context)


@login_required
def my_reservations(request):
    """View user's reservations"""
    reservations = Reservation.objects.filter(user=request.user).order_by('-date', '-time')
    context = {
        'reservations': reservations,
    }
    return render(request, 'main/my_reservations.html', context)


# ==================== ADMIN DASHBOARD ====================

def is_staff(user):
    """Check if user is staff"""
    return user.is_staff or user.is_superuser


@login_required
@user_passes_test(is_staff)
def admin_dashboard(request):
    """Admin dashboard overview"""
    # Statistics
    total_orders = Order.objects.count()
    pending_orders = Order.objects.filter(status__in=['pending', 'paid', 'preparing']).count()
    total_reservations = Reservation.objects.count()
    upcoming_reservations = Reservation.objects.filter(
        date__gte=timezone.now().date(),
        status='confirmed'
    ).count()
    
    # Recent activity
    recent_orders = Order.objects.all()[:10]
    recent_reservations = Reservation.objects.all()[:10]
    
    context = {
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'total_reservations': total_reservations,
        'upcoming_reservations': upcoming_reservations,
        'recent_orders': recent_orders,
        'recent_reservations': recent_reservations,
    }
    return render(request, 'main/admin/dashboard.html', context)


@login_required
@user_passes_test(is_staff)
def admin_orders(request):
    """View all orders"""
    status_filter = request.GET.get('status', '')
    
    if status_filter:
        orders = Order.objects.filter(status=status_filter)
    else:
        orders = Order.objects.all()
    
    context = {
        'orders': orders,
        'status_choices': Order.STATUS_CHOICES,
        'selected_status': status_filter,
    }
    return render(request, 'main/admin/orders.html', context)


@login_required
@user_passes_test(is_staff)
def admin_order_detail(request, order_id):
    """View order details"""
    order = get_object_or_404(Order, id=order_id)
    context = {
        'order': order,
        'status_choices': Order.STATUS_CHOICES,
    }
    return render(request, 'main/admin/order_detail.html', context)


@login_required
@user_passes_test(is_staff)
def admin_update_order_status(request, order_id):
    """Update order status"""
    if request.method == 'POST':
        order = get_object_or_404(Order, id=order_id)
        new_status = request.POST.get('status')
        
        order.status = new_status
        order.save()
        
        # Send email notification
        user_email = order.guest_email if order.guest_email else (order.user.email if order.user else None)
        user_name = order.guest_name if order.guest_name else (order.user.username if order.user else 'Customer')
        
        if user_email:
            try:
                send_mail(
                    f'Order Status Update - {order.order_number}',
                    f'Hi {user_name},\n\nYour order status has been updated to: {order.get_status_display()}\n\nOrder Number: {order.order_number}',
                    settings.DEFAULT_FROM_EMAIL,
                    [user_email],
                    fail_silently=True,
                )
            except:
                pass
        
        messages.success(request, 'Order status updated successfully!')
    
    return redirect('main:admin_order_detail', order_id=order_id)


@login_required
@user_passes_test(is_staff)
def admin_reservations(request):
    """View all reservations"""
    status_filter = request.GET.get('status', '')
    date_filter = request.GET.get('date', '')
    
    reservations = Reservation.objects.all()
    
    if status_filter:
        reservations = reservations.filter(status=status_filter)
    
    if date_filter:
        try:
            date = datetime.strptime(date_filter, '%Y-%m-%d').date()
            reservations = reservations.filter(date=date)
        except ValueError:
            pass
    
    context = {
        'reservations': reservations,
        'status_choices': Reservation.STATUS_CHOICES,
        'selected_status': status_filter,
        'selected_date': date_filter,
    }
    return render(request, 'main/admin/reservations.html', context)


@login_required
@user_passes_test(is_staff)
def admin_update_reservation_status(request, reservation_id):
    """Update reservation status"""
    if request.method == 'POST':
        reservation = get_object_or_404(Reservation, id=reservation_id)
        new_status = request.POST.get('status')
        
        reservation.status = new_status
        reservation.save()
        
        # Send email notification
        user_email = reservation.guest_email if reservation.guest_email else (reservation.user.email if reservation.user else None)
        user_name = reservation.guest_name if reservation.guest_name else (reservation.user.username if reservation.user else 'Guest')
        
        if user_email:
            try:
                send_mail(
                    f'Reservation Status Update - {reservation.reservation_number}',
                    f'Hi {user_name},\n\nYour reservation status has been updated to: {reservation.get_status_display()}\n\nReservation Number: {reservation.reservation_number}',
                    settings.DEFAULT_FROM_EMAIL,
                    [user_email],
                    fail_silently=True,
                )
            except:
                pass
        
        messages.success(request, 'Reservation status updated successfully!')
    
    return redirect('main:admin_reservations')
