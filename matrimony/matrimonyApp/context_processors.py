# context_processors.py

from .models import PaymentDetail

def subscription_info(request):
    has_subscription = False
    subscription_type = "Free User"
    amount_total = None
    
    if request.user.is_authenticated:
        payment_detail = PaymentDetail.objects.filter(user=request.user).first()
        if payment_detail and payment_detail.status == 'active' and payment_detail.payment_status == 'paid':
            has_subscription = True
            if payment_detail.session_mode == 'subscription':
                subscription_type = 'Subscribed User'
            else:
                subscription_type = 'Paid User'
            amount_total = payment_detail.amount_total

    return {
        'has_subscription': has_subscription,
        'subscription_type': subscription_type,
        'amount_total': amount_total,
    }
