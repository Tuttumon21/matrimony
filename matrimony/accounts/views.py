from django.shortcuts import render, redirect,reverse
from.forms import LoginForm, RegistrationForm, ProfileUpdateForm, BasicInfoForm, LifeStyleForm, EmploymentStatusForm,RelationshipTypeForm
from django.contrib.auth import authenticate, login, logout
from .models import User
from django.forms.forms import BaseForm
from django.urls import reverse_lazy
from typing import Any
from django.views.generic import View, TemplateView, DetailView, UpdateView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.
class LoginView(View):
    def get(self, request):
        context = {}
        context['form'] = LoginForm()
        return render(request, 'accounts/login.html', context)
    
    def post(self, request):
        context = {}
        form = LoginForm(request.POST)
        context['form'] = form
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            try:
                user_from_db = User.objects.get(email=email)
                username = user_from_db.username
                user = authenticate(request, username=username, password=password)
                if not user:
                    return render(request, 'accounts/login.html', context)

                login(request, user)
                return redirect('/')
                # return redirect('matrimonyApp:home')

            except User.DoesNotExist:
                return render(request, 'accounts/login.html', context)
            
        return render(request, 'accounts/login.html', context)

def user_registration(request):
    context = {}
    if request.method == 'GET':
        context['form'] = RegistrationForm()
        return render(request, 'accounts/register.html', context)

    elif request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        context['form'] = form

        if not form.is_valid():
            return render(request, 'accounts/register.html', context)

        try:
            user = form.save(commit=False)
            user.set_password(user.password)
            user.save()
            login(request, user)
            # return redirect(reverse('accounts:basic_info'))
            return redirect(reverse('accounts:basic_info'))

        except:
            return render(request, 'accounts/register.html', context)

class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        return redirect('/')

class ProfileView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/profile_view.html'
    
    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        context['data'] = self.request.user
        return context

class ProfileUpdateView(LoginRequiredMixin, FormView):
    model = User
    form_class = ProfileUpdateForm
    template_name = 'accounts/profile_update.html'
    success_url = reverse_lazy('accounts:profile')

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()
        return form_class(instance=self.request.user, **self.get_form_kwargs())
    
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

class ChangePasswordView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/change_password.html'

def basic_info_view(request):
    if request.method == 'POST':
        form = BasicInfoForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect(reverse('accounts:lifestyle_info'))  # Change to your desired redirect URL
    else:
        form = BasicInfoForm(instance=request.user)
    return render(request, 'accounts/basic_info.html', {'form': form})

def lifestyle_view(request):
    if request.method == 'POST':
        form = LifeStyleForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect(reverse('accounts:employment_status'))
    else:
        form = LifeStyleForm(instance=request.user)
    return render(request, 'accounts/lifestyle_form.html', {'form': form})

def employment_status_view(request):
    if request.method == 'POST':
        form = EmploymentStatusForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect(reverse('accounts:relationship_type'))
    else:
        form = EmploymentStatusForm(instance=request.user)
    return render(request, 'accounts/employment_info.html', {'form': form})

def relationship_type_view(request):
    if request.method == 'POST':
        form = RelationshipTypeForm(request.POST, instance=request.user)
        if form.is_valid():
            relationship_type_instance = form.save()

            if relationship_type_instance.relationship_type == 'short_term':
                return redirect('datingapp_dashboard')  # URL name for the dating app dashboard
            else:
                return redirect('/')  # URL name for the matrimony app dashboard
    else:
        form = RelationshipTypeForm(instance=request.user)
    return render(request, 'accounts/relationship_type.html', {'form': form})
