from apps.core.emailing import send_system_email


def notify_order_status_updated(order):
    if not order.customer or not order.customer.email:
        return 0
    return send_system_email(
        subject=f"Order {order.order_number} updated",
        message=f"Your order is now marked as {order.status}.",
        recipient_list=[order.customer.email],
    )
