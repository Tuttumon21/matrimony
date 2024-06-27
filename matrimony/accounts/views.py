from django.shortcuts import render, redirect
from.forms import LoginForm, RegistrationForm, ProfileUpdateForm
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

            except User.DoesNotExist:
                return render(request, 'accounts/login.html', context)
            
        return render(request, 'accounts/login.html', context)

def user_registration(request):
    context = {}
    if request.method == 'GET':
        context['form'] = RegistrationForm()
        return render(request, 'accounts/register.html', context)

    elif request.method == 'POST':
        form = LoginForm(data=request.POST)
        context['form'] = form

        if not form.is_valid():
            return render(request, 'accounts/register.html', context)

        try:
            user = form.save(commit=False)
            user.save()
            login(request, user)
            return redirect('/')

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

    def get_form(self):
        return self.form_class(instance=self.request.user)
    
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

class ChangePasswordView(LoginRequiredMixin, TemplateView):
    template_name = 'accounts/change_password.html'