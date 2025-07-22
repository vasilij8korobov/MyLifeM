from django.shortcuts import redirect, render


def home(request):
    if request.user.is_authenticated:
        context = {}

        if hasattr(request.user, 'school_diary'):
            context['school_diary'] = request.user.school_diary
        return render(request, 'diary/home.html', context)
    return redirect('login')
