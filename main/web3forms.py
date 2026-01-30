"""
Web3Forms Email Integration
Send confirmation emails via Web3Forms API
"""
import requests
import json


def send_web3forms_email(access_key, to_email, subject, message, from_name="Restaurant"):
    """
    Send email using Web3Forms API
    
    Args:
        access_key: Your Web3Forms access key
        to_email: Recipient email address
        subject: Email subject
        message: Email message body
        from_name: Sender name (default: Restaurant)
    
    Returns:
        dict: Response from Web3Forms API
    """
    url = "https://api.web3forms.com/submit"
    
    data = {
        "access_key": access_key,
        "subject": subject,
        "email": to_email,
        "name": from_name,
        "message": message,
    }
    
    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"success": False, "error": str(e)}


def send_order_confirmation(access_key, order):
    """Send order confirmation email via Web3Forms"""
    email = order.guest_email if order.guest_email else (order.user.email if order.user else "")
    name = order.guest_name if order.guest_name else (order.user.username if order.user else "Customer")
    
    if not email:
        return {"success": False, "error": "No email address provided"}
    
    subject = f"Order Confirmation - {order.order_number}"
    
    message = f"""
Hi {name},

Thank you for your order! Your order has been confirmed.

Order Details:
--------------
Order Number: {order.order_number}
Order Type: {order.get_order_type_display()}
Total Amount: £{order.total}
Status: {order.get_status_display()}

"""
    
    if order.order_type == 'delivery':
        message += f"Delivery Address: {order.delivery_address}\n"
        message += f"Delivery Fee: £{order.delivery_fee}\n"
    
    message += "\nWe will notify you when your order is being prepared.\n\n"
    message += "Thank you for choosing our restaurant!\n\n"
    message += "Best regards,\nRestaurant Team"
    
    return send_web3forms_email(access_key, email, subject, message, from_name="Restaurant")


def send_reservation_confirmation(access_key, reservation):
    """Send reservation confirmation email via Web3Forms"""
    email = reservation.guest_email if reservation.guest_email else (reservation.user.email if reservation.user else "")
    name = reservation.guest_name if reservation.guest_name else (reservation.user.username if reservation.user else "Guest")
    
    if not email:
        return {"success": False, "error": "No email address provided"}
    
    subject = f"Reservation Confirmation - {reservation.reservation_number}"
    
    message = f"""
Hi {name},

Your table reservation has been confirmed!

Reservation Details:
-------------------
Reservation Number: {reservation.reservation_number}
Date: {reservation.date.strftime('%B %d, %Y')}
Time: {reservation.time.strftime('%I:%M %p')}
Number of Guests: {reservation.guests}
Status: {reservation.get_status_display()}

"""
    
    if reservation.special_requests:
        message += f"Special Requests: {reservation.special_requests}\n\n"
    
    message += "We look forward to serving you!\n\n"
    
    if reservation.guest_phone:
        message += f"If you need to make any changes, please contact us at your earliest convenience.\n"
        message += f"Your contact number: {reservation.guest_phone}\n\n"
    
    message += "Best regards,\nRestaurant Team"
    
    return send_web3forms_email(access_key, email, subject, message, from_name="Restaurant")


def send_admin_notification(access_key, admin_email, notification_type, details):
    """Send notification to admin about new orders/reservations"""
    subject = f"New {notification_type} Notification"
    
    message = f"""
New {notification_type} received!

{details}

Please check the admin dashboard for more details.

Best regards,
Restaurant System
"""
    
    return send_web3forms_email(access_key, admin_email, subject, message, from_name="Restaurant System")
