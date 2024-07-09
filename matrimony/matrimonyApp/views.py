from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from .forms import ParentsDetailsForm,PartnerPreferenceForm
from django.contrib.auth.decorators import login_required
from .models import ParentsDetails,PartnerPreference
from django.contrib.auth.mixins import LoginRequiredMixin
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

