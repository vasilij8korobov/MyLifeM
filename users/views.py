from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from .forms import SignUpForm


def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        print("Form data:", request.POST)  # Отладочная печать
        if form.is_valid():
            print("Form is valid")  # Проверка валидности
            user = form.save()
            print("User created:", user)  # Проверка создания пользователя

            login(request, user)
            return redirect('home')
        else:
            print("Form errors:", form.errors)  # Печать ошибок формы
    else:
        form = SignUpForm()

    return render(request, 'users/register.html', {'form': form})


class CustomLoginView(SuccessMessageMixin, LoginView):
    template_name = 'users/login.html'
    redirect_authenticated_user = True  # Авторизованных перенаправляет на главную
    success_message = "Добро пожаловать, %(username)s!"

    def get_success_url(self):
        return reverse_lazy('diary_list')  # Перенаправляем на home после входа


class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        messages.info(request, "Вы успешно вышли из системы")
        return super().dispatch(request, *args, **kwargs)
