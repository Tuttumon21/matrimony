from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView,FormView,ListView
from .forms import ParentsDetailsForm,PartnerPreferenceForm,FriendRequestForm
from django.contrib.auth.decorators import login_required
from .models import ParentsDetails,PartnerPreference,FriendRequest,ProfileExclusion
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.models import User
from django.db.models import Q
from django.views import View
from django.urls import reverse
from django.views.generic import ListView
# from django.utils.decorators import method_decorator
# from django.urls import reverse_lazy
# from django.http import JsonResponse

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        try:
            partner_preference = user.partner_preference
            friends = FriendRequest.objects.filter(
                Q(from_user=user) | Q(to_user=user),
                status='accepted'
            ).values_list('from_user', 'to_user')
            friend_ids = [item for sublist in friends for item in sublist if item != user.id]
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
            ).exclude(id__in=friend_ids).exclude(id=user.id).select_related('partner_preference').prefetch_related('parents_details')
            context['profiles'] = profiles
        except PartnerPreference.DoesNotExist:
            context['profiles'] = User.objects.none()

        return context

# class SuggestionView(LoginRequiredMixin, TemplateView):
#     template_name = 'suggestions.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         user = self.request.user

#         try:
#             partner_preference = user.partner_preference

#             accepted_friend_requests = FriendRequest.objects.filter(
#                 from_user=user, status='accepted'
#             ).values_list('to_user', flat=True)

#             exclusions = ProfileExclusion.objects.filter(
#                 user=user
#             ).values_list('excluded_profile', flat=True)

#             profiles = User.objects.filter(
#                 age__gte=partner_preference.age_min,
#                 age__lte=partner_preference.age_max,
#                 # parents_details__caste=partner_preference.caste,
#                 # parents_details__religion=partner_preference.religion,
#                 # parents_details__height__gte=partner_preference.height_min,
#                 # parents_details__height__lte=partner_preference.height_max,
#                 # parents_details__weight__gte=partner_preference.weight_min,
#                 # parents_details__weight__lte=partner_preference.weight_max,
#                 # parents_details__annual_income__gte=partner_preference.income_min,
#                 # parents_details__annual_income__lte=partner_preference.income_max,
#                 # education_level=partner_preference.qualification
#             ).exclude(id=user.id).exclude(id__in=accepted_friend_requests).exclude(id__in=exclusions).select_related('partner_preference').prefetch_related('parents_details')
#             context['profiles'] = profiles
#         except PartnerPreference.DoesNotExist:
#             profiles = User.objects.none()

#         return context

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
# @login_required
# def friends_list(request):
#     # Fetch accepted friend requests where the current user is either the sender or receiver
#     accepted_requests = FriendRequest.objects.filter(status='accepted').filter(
#         (Q(from_user=request.user) | Q(to_user=request.user))
#     )
    
#     # Extract friends from accepted friend requests
#     friends = []
#     for req in accepted_requests:
#         if req.from_user == request.user:
#             friends.append(req.to_user)
#         else:
#             friends.append(req.from_user)
    
#     context = {
#         'friends': friends,
#     }
    
#     return render(request, 'friends_list.html', context)

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

