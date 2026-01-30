from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    # Public pages
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('locations/', views.locations, name='locations'),
    
    # Menu
    path('menu/', views.menu, name='menu'),
    path('menu/<int:item_id>/', views.menu_detail, name='menu_detail'),
    
    # Authentication
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
    
    # Ordering system
    path('basket/', views.basket, name='basket'),
    path('add-to-basket/<int:item_id>/', views.add_to_basket, name='add_to_basket'),
    path('update-basket/<int:item_id>/', views.update_basket, name='update_basket'),
    path('remove-from-basket/<int:item_id>/', views.remove_from_basket, name='remove_from_basket'),
    path('checkout/', views.checkout, name='checkout'),
    path('process-payment/', views.process_payment, name='process_payment'),
    path('order-confirmation/<str:order_number>/', views.order_confirmation, name='order_confirmation'),
    
    # Reservations
    path('reservations/', views.make_reservation, name='make_reservation'),
    path('reservation-confirmation/<str:reservation_number>/', views.reservation_confirmation, name='reservation_confirmation'),
    path('my-reservations/', views.my_reservations, name='my_reservations'),
    
    # Admin dashboard
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-orders/', views.admin_orders, name='admin_orders'),
    path('admin-order/<int:order_id>/', views.admin_order_detail, name='admin_order_detail'),
    path('admin-update-order-status/<int:order_id>/', views.admin_update_order_status, name='admin_update_order_status'),
    path('admin-reservations/', views.admin_reservations, name='admin_reservations'),
    path('admin-update-reservation/<int:reservation_id>/', views.admin_update_reservation_status, name='admin_update_reservation_status'),
]
