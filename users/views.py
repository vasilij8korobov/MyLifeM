from django.contrib.auth import login
from django.shortcuts import render, redirect

from diary.models import SchoolDiary
from .forms import SignUpForm


def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()

            # Создаем школьный дневник, если пользователь младше 18 И выбрал опцию
            if user.is_minor and form.cleaned_data['wants_school_diary']:
                SchoolDiary.objects.create(user=user)  # Создаем пустую запись

            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()

    return render(request, 'registration/register.html', {'form': form})