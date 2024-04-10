from django.http import HttpResponseRedirect
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.views.generic.edit import CreateView
from django.contrib import messages
from products.mixins import BaseMixin
from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm
from django.urls import reverse, reverse_lazy
from users.models import User
from django.contrib import auth
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.views.generic import ListView, DetailView
from basket.models import Favorites
from django.db.models.base import Model as Model


class UserLoginView(BaseMixin, LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    success_url = reverse_lazy('products:home')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"Добро пожаловать, {self.request.user.first_name}")
        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.error(self.request, "Пожалуйста, убедитесь в правильности ввода данных.")
        return response


class UserRegistrationView(CreateView):
    model = User
    template_name = 'users/registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('users:login')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, f"Поздравляем. Вы успешно зарегистрировались!")
        return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        messages.error(self.request, "Пожалуйста, убедитесь в правильности ввода данных.")
        return response


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('products:home'))


def details(request):
    if request.method == 'POST':
        form = UserProfileForm(instance=request.user, data=request.POST)
        print(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Данные успешно изменены!")
            return HttpResponseRedirect(reverse('users:details'))
        else:
            messages.error(request, "Проверьте правильность ввода данных!")
            return HttpResponseRedirect(reverse('users:details'))
    else:
        context = {'title': 'Личные данные', 'form': UserProfileForm(instance=request.user)}
        return render(request, 'users/details.html', context)


class ProfileView(BaseMixin, DetailView):
    model = User
    template_name = 'users/profile.html'
    title = 'StuffStore - Профиль'

    def get_object(self, queryset=None) -> Model:
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['favorites_products'] = Favorites.objects.filter(user=self.request.user)
        return context
