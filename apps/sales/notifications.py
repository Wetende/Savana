from apps.core.emailing import send_system_email


def notify_inquiry_received(inquiry):
    send_system_email(
        subject="Wholesale inquiry received",
        message=f"Thanks {inquiry.full_name}, we received your inquiry.",
        recipient_list=[inquiry.email],
    )


def notify_quote_sent(quote):
    email = quote.customer.email if quote.customer else getattr(quote.inquiry, "email", None)
    if not email:
        return 0
    return send_system_email(
        subject=f"Quote {quote.reference} sent",
        message=f"Your quote {quote.reference} is ready.",
        recipient_list=[email],
    )


def notify_quote_accepted(quote):
    email = quote.customer.email if quote.customer else getattr(quote.inquiry, "email", None)
    if not email:
        return 0
    return send_system_email(
        subject=f"Quote {quote.reference} accepted",
        message=f"Quote {quote.reference} has been accepted.",
        recipient_list=[email],
    )
