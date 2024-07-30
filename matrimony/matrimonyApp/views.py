from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView,FormView,ListView
from .forms import ParentsDetailsForm,PartnerPreferenceForm,FriendRequestForm,MessageForm,SaveProfileForm
from django.contrib.auth.decorators import login_required
from .models import ParentsDetails,PartnerPreference,FriendRequest,ProfileExclusion,Message,Subscription,PaymentDetail, SavedProfile
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.models import User
from django.db.models import Q,Max
from django.views import View
from django.urls import reverse

from django.http import JsonResponse
import json
import stripe
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import HttpResponse
from django.conf import settings
# from django.utils.decorators import method_decorator
# from django.urls import reverse_lazy


# Create your views here.


# Create your views here.

class HomeView(LoginRequiredMixin,TemplateView):
    template_name = 'home.html'

@login_required
def parents_details_view(request):
    try:
        parents_details = request.user.parents_details
    except ParentsDetails.DoesNotExist:
        parents_details = ParentsDetails(user=request.user)

    if request.method == 'POST':
        form = ParentsDetailsForm(request.POST, request.FILES, instance=parents_details)
        if form.is_valid():
            form.save()
            return redirect('matrimonyApp:partner_preference')
    else:
        form = ParentsDetailsForm(instance=parents_details)
    
    return render(request, 'parents_details_form.html', {'form': form})

@login_required
def partner_preference_view(request):
    try:
        partner_preference = request.user.partner_preference
    except PartnerPreference.DoesNotExist:
        partner_preference = None

    if request.method == 'POST':
        form = PartnerPreferenceForm(request.POST, instance=partner_preference)
        if form.is_valid():
            partner_preference = form.save(commit=False)
            partner_preference.user = request.user
            partner_preference.save()
            return redirect('matrimonyApp:home')
    else:
        form = PartnerPreferenceForm(instance=partner_preference)

    context = {'form': form}
    return render(request, 'partner_preference_form.html', context)

class SuggestionView(LoginRequiredMixin, TemplateView):
    template_name = 'suggestions.html'

    def get_gender_filter(self, interested_gender):
        if interested_gender == 'MALE':
            return Q(gender='MALE')
        elif interested_gender == 'FEMALE':
            return Q(gender='FEMALE')
        else:
            return Q(gender__in=['MALE', 'FEMALE'])
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        try:
            partner_preference = user.partner_preference
            interested_gender = user.parents_details.interested_gender
            friends = FriendRequest.objects.filter(
                Q(from_user=user) | Q(to_user=user),
                status='accepted'
            ).values_list('from_user', 'to_user')
            friend_ids = [item for sublist in friends for item in sublist if item != user.id]
            gender_filter = self.get_gender_filter(interested_gender)
            profiles = User.objects.filter(
                age__gte=partner_preference.age_min,
                age__lte=partner_preference.age_max,
                parents_details__caste=partner_preference.caste,
                parents_details__religion=partner_preference.religion,
                parents_details__height__gte=partner_preference.height_min,
                parents_details__height__lte=partner_preference.height_max,
                parents_details__weight__gte=partner_preference.weight_min,
                parents_details__weight__lte=partner_preference.weight_max,
                parents_details__annual_income__gte=partner_preference.income_min,
                parents_details__annual_income__lte=partner_preference.income_max,
                education_level=partner_preference.qualification
            ).filter(gender_filter).exclude(id__in=friend_ids).exclude(id=user.id).select_related('partner_preference').prefetch_related('parents_details')
            context['profiles'] = profiles
        except PartnerPreference.DoesNotExist:
            context['profiles'] = User.objects.none()

        return context

@login_required
def send_request(request, profile_id):
    to_user = get_object_or_404(User, id=profile_id)
    from_user = request.user
    if request.method == 'POST':
        if not FriendRequest.objects.filter(from_user=from_user, to_user=to_user).exists():
            FriendRequest.objects.create(from_user=from_user, to_user=to_user)
    return redirect('matrimonyApp:suggestions')

@login_required
def respond_to_request(request, request_id, action):
    friend_request = get_object_or_404(FriendRequest, id=request_id, to_user=request.user)
    
    if action == 'accept':
        friend_request.status = 'accepted'
    elif action == 'reject':
        friend_request.status = 'rejected'
    friend_request.save()
    
    return redirect('matrimonyApp:view_requests')

@login_required
def view_requests(request):
    received_requests = FriendRequest.objects.filter(to_user=request.user, status='pending')
    sent_requests = FriendRequest.objects.filter(from_user=request.user, status='pending')
    
    context = {
        'received_requests': received_requests,
        'sent_requests': sent_requests,
    }
    
    return render(request, 'requests.html', context)

class FriendsListView(LoginRequiredMixin, ListView):
    template_name = 'friends_list.html'
    context_object_name = 'friends'

    def get_queryset(self):
        return FriendRequest.objects.filter(
            Q(from_user=self.request.user) | Q(to_user=self.request.user),
            status='accepted'
        ).select_related('from_user', 'to_user')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Check if the user has an active, paid plan
        has_active_paid_plan = PaymentDetail.objects.filter(
            user=self.request.user,
            status='active',
            payment_status='paid'
        ).exists()
        context['has_active_paid_plan'] = has_active_paid_plan
        return context

@login_required
def save_profile(request, profile_id):
    profile = get_object_or_404(User, id=profile_id)
    saved_profile, created = SavedProfile.objects.get_or_create(user=request.user, saved_profile=profile)
    if created:
        saved_profile.save()
    return redirect('matrimonyApp:suggestions')

@login_required
def saved_profiles(request):
    saved_profiles = SavedProfile.objects.filter(user=request.user).select_related('saved_profile', 'saved_profile__parents_details')
    return render(request, 'saved_profiles.html', {'saved_profiles': saved_profiles})

@login_required
def unfriend(request, user_id):
    friend_request = get_object_or_404(FriendRequest, from_user=request.user, to_user__id=user_id, status='accepted')
    friend_request.unfriend()
    return redirect('matrimonyApp:friends_list')  # Redirect to your friends list page

class ExcludeProfileView(LoginRequiredMixin, View):
    def post(self, request, profile_id):
        profile = get_object_or_404(User, id=profile_id)
        exclusion, created = ProfileExclusion.objects.get_or_create(user=request.user, excluded_profile=profile)
        return redirect('matrimonyApp:suggestions')

@login_required
def send_message(request, recipient_id):
    recipient = get_object_or_404(User, id=recipient_id)
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.recipient = recipient
            message.save()
            return redirect('matrimonyApp:chat_room', friend_id=recipient.id)
    else:
        form = MessageForm(initial={'recipient': recipient})
    return render(request, 'send_message.html', {'form': form, 'recipient': recipient})

@login_required
def chat_room(request, friend_id):
    friend = get_object_or_404(User, id=friend_id)
    messages = Message.objects.filter(
        Q(sender=request.user, recipient=friend) | Q(sender=friend, recipient=request.user)
    ).order_by('timestamp')
    
    user = request.user
    friends = FriendRequest.objects.filter(
        Q(from_user=user, status='accepted') | Q(to_user=user, status='accepted')
    )

    if request.method == 'POST':
        body = request.POST.get('body')
        if body:
            Message.objects.create(sender=request.user, recipient=friend, body=body)
            return redirect('matrimonyApp:chat_room', friend_id=friend.id)

    return render(request, 'chat_room.html', {'friend': friend, 'messages': messages, 'friends': friends})

def chat_with_friends(request, room_name=None):
    user = request.user
    friends = FriendRequest.objects.filter(
        Q(from_user=user, status='accepted') | Q(to_user=user, status='accepted')
    )

    
    friends_with_last_message = friends.annotate(
        last_message_time=Max('to_user__received_messages__timestamp')
    ).order_by('-last_message_time')

    
    friend = None
    messages = []
    if room_name:
        friend = get_object_or_404(User, username=room_name)
        messages = Message.objects.filter(
            (Q(sender=user) & Q(recipient=friend)) |
            (Q(sender=friend) & Q(recipient=user))
        ).order_by('timestamp')
    
    if request.method == 'POST':
        body = request.POST.get('body')
        if body:
            Message.objects.create(sender=request.user, recipient=friend, body=body)

    return render(request, 'chat_with_friends.html', {
        'friends': friends_with_last_message,
        'friend': friend,
        'messages': messages,
    })

class ProfileDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'profile_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile_id = self.kwargs.get('profile_id')
        profile = get_object_or_404(User, id=profile_id)
        context['profile'] = profile
        return context


stripe.api_key = settings.STRIPE_SECRET_KEY
# class SubscriptionView(LoginRequiredMixin, TemplateView):
#     template_name = 'payments/subscription.html'
class SubscriptionView(LoginRequiredMixin, TemplateView):
    template_name = 'payments/subscription.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['CUSTOMER_EMAIL'] = self.request.user.email
        context['PRICING_TABLE_ID'] = settings.PRICING_TABLE_ID
        context['STRIPE_PUBLISHABLE_KEY'] = settings.STRIPE_PUBLISHABLE_KEY
        context['PAYMENT_METHOD_TYPES']=["card","link"]
        return context
    

#testing endpoint key
def update_payment_detail(session_data=None, charge_data=None, invoice_data=None):
    print("Inside update_payment_detail")
    #for payment method save
    if session_data:
        email = session_data['customer_email']
        payment_intent = session_data['payment_intent']
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            print(f'User with email {email} does not exist.')
            return
        
        PaymentDetail.objects.filter(user=user).delete()

        update_fields = {
            'session_mode': session_data.get('session_mode', None),
            'customer_id': session_data.get('customer_id', None),
            'amount_total': session_data.get('amount_total', None),
            'currency': session_data.get('currency', None),
            'payment_status': session_data.get('payment_status', None),
            'customer_email': session_data.get('customer_email', None),
            'customer_name': session_data.get('customer_name', None),
            'customer_phone': session_data.get('customer_phone', None),
            'status': 'active' if session_data.get('payment_status') == 'paid' else 'inactive',
            'receipt_url': charge_data.get('receipt_url') if charge_data else None,
            'payment_method_type': charge_data.get('payment_method_type') if charge_data else None,
            'hosted_invoice_url': invoice_data.get('hosted_invoice_url') if invoice_data else None,
            'subscription_id': invoice_data.get('subscription_id') if invoice_data else None,
            'description': invoice_data.get('description') if invoice_data else None,
            'invoice_id': invoice_data.get('invoice_id') if invoice_data else None
        }

        payment_detail, created = PaymentDetail.objects.update_or_create(
            user=user,
            payment_intent=payment_intent,
            defaults=update_fields
        )
        
        print(f"Created or updated payment detail for {email}")
    
    #for subscription Method save
    if invoice_data:
        email = invoice_data['customer_email']
        payment_intent = invoice_data['payment_intent']
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            print(f'User with email {email} does not exist.')
            return
        
        PaymentDetail.objects.filter(user=user).delete()
        
        update_fields = {
            'session_mode': invoice_data.get('session_mode', None),
            'customer_id': invoice_data.get('customer_id', None),
            'amount_total': invoice_data.get('amount_total', None),
            'currency': invoice_data.get('currency', None),
            'payment_status': invoice_data.get('payment_status', None),
            'customer_email': invoice_data.get('customer_email', None),
            'customer_name': invoice_data.get('customer_name', None),
            'customer_phone': invoice_data.get('customer_phone', None),
            'status': 'active' if invoice_data.get('payment_status') == 'paid' else 'inactive',
            'receipt_url': charge_data.get('receipt_url') if charge_data else None,
            'payment_method_type': charge_data.get('payment_method_type') if charge_data else None,
            'hosted_invoice_url': invoice_data.get('hosted_invoice_url') if invoice_data else None,
            'subscription_id': invoice_data.get('subscription_id') if invoice_data else None,
            'description': invoice_data.get('description') if invoice_data else None,
            'invoice_id': invoice_data.get('invoice_id') if invoice_data else None
        }

        payment_detail, created = PaymentDetail.objects.update_or_create(
            user=user,
            payment_intent=payment_intent,
            defaults=update_fields
        )
        
        print(f"Created or updated payment detail for {email}")


endpoint_secret = 'whsec_651aa94a96b549741c7d2c99f67f5ac0965f9131c2206ae0db227b92a1f1d439'
event_data_storage = {}


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.headers['STRIPE_SIGNATURE']
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        print(f'ValueError: {e}')
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        print(f'SignatureVerificationError: {e}')
        return HttpResponse(status=400)

    # Handle the event

    event_type = event['type']
    data = event['data']['object']
    payment_intent = data.get('payment_intent', None)
    customer_email = data.get('customer_email', None)

    if payment_intent:
        if payment_intent not in event_data_storage:
            event_data_storage[payment_intent] = {}
    
        if event_type == 'checkout.session.completed':
            event_data_storage[payment_intent]['session_data'] = {
                'session_mode': data['mode'],
                'customer_id': data['customer'],
                'amount_total': data['amount_total'],
                'currency': data['currency'],
                'payment_status': data['payment_status'],
                'customer_email': data['customer_details']['email'],
                'customer_name': data['customer_details']['name'],
                'customer_phone': data['customer_details']['phone'],
                'payment_intent': data['payment_intent']
            }
            print(f"Stored session data for payment_intent {payment_intent}")

        elif event_type == 'charge.succeeded':
            event_data_storage[payment_intent]['charge_data'] = {
                'receipt_url': data.get('receipt_url'),
                'payment_method_type': data['payment_method_details']['type'],
                'customer_email': data['billing_details']['email'],
                'payment_intent': data['payment_intent']
            }
            print(f"Stored charge data for payment_intent {payment_intent}")

        elif event_type == 'invoice.payment_succeeded':
            event_data_storage[payment_intent]['invoice_data'] = {
                'hosted_invoice_url': data['hosted_invoice_url'],
                'subscription_id': data['subscription'],
                'description': data['lines']['data'][0]['description'] if data['lines']['data'] else None,
                'customer_email': data['customer_email'],
                'invoice_id': data['id'],
                'payment_intent': data['payment_intent'],
                'customer_email': data['customer_email'],
                'customer_name': data['customer_name'],
                'customer_phone': data['customer_phone'],
                'payment_status': data['status'],
                'currency': data['currency'],
                'amount_total': data['total'],
                'customer_id': data['customer'],
                'session_mode': data['lines']['data'][0]['type'] if data['lines']['data'] else None,
            }
            print(f"Stored invoice data for payment_intent {payment_intent}")
            # print(event_data_storage[payment_intent]['invoice_data'])

        # Attempt to update the payment details if all required data is present
        if payment_intent in event_data_storage:
            session_data = event_data_storage[payment_intent].get('session_data', None)
            charge_data = event_data_storage[payment_intent].get('charge_data', None)
            invoice_data = event_data_storage[payment_intent].get('invoice_data', None)
            

            if session_data and (charge_data or invoice_data):
                print("Attempting to update payment detail for Payment Method...")
                update_payment_detail(session_data=session_data, charge_data=charge_data, invoice_data=invoice_data)
                # Cleanup after processing
                del event_data_storage[payment_intent]
            elif charge_data and (session_data or invoice_data):
                print("Attempting to update payment detail for Subscription Method...")
                update_payment_detail(session_data=session_data, charge_data=charge_data, invoice_data=invoice_data)
                # Cleanup after processing
                del event_data_storage[payment_intent]

    return HttpResponse(status=200)



class SuccessPremiumView(View):
  def get(self, request, checkout_session_id, *args, **kwargs):
    # Retrieve the checkout session from Stripe
    session = stripe.checkout.Session.retrieve(checkout_session_id)
    
    return render(request, 'payments/SuccessPremium.html', {'session': session})
class SuccessBasicView(View):
  def get(self, request, checkout_session_id, *args, **kwargs):
    # Retrieve the checkout session from Stripe
    session = stripe.checkout.Session.retrieve(checkout_session_id)
    
    return render(request, 'payments/SuccessBasic.html', {'session': session})

class CancelView(TemplateView):
    template_name = 'cancel.html'