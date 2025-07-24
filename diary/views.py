from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from diary.forms import GradeForm, DiaryEntryForm
from diary.mixins import OwnerRequiredMixin
from diary.models import DiaryEntry, GradeRecord


def home(request):
    context = {
        'show_school_diary': hasattr(request.user, 'schooldiary') if request.user.is_authenticated else False
    }
    return render(request, 'diary/base.html', context)

# Основной дневник
class DiaryListView(LoginRequiredMixin, ListView):
    model = DiaryEntry
    template_name = 'diary/diary_list.html'
    context_object_name = 'entries'

    def get_queryset(self):
        return DiaryEntry.objects.filter(user=self.request.user)

class DiaryCreateView(LoginRequiredMixin, CreateView):
    model = DiaryEntry
    form_class = DiaryEntryForm
    template_name = 'diary/diary_form.html'
    success_url = reverse_lazy('diary_list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class DiaryUpdateView(LoginRequiredMixin, OwnerRequiredMixin, UpdateView):
    model = DiaryEntry
    fields = ['title', 'text', 'is_private']
    template_name = 'diary/diary_form.html'
    success_url = reverse_lazy('diary_list')

    def get_queryset(self):
        return DiaryEntry.objects.filter(user=self.request.user)

class DiaryDeleteView(LoginRequiredMixin, OwnerRequiredMixin, DeleteView):
    model = DiaryEntry
    template_name = 'diary/diary_confirm_delete.html'
    success_url = reverse_lazy('diary_list')

    def get_queryset(self):
        return DiaryEntry.objects.filter(user=self.request.user)

# Школьный дневник
class SchoolDiaryView(LoginRequiredMixin, ListView):
    model = GradeRecord
    template_name = 'diary/school_diary.html'
    context_object_name = 'grades'

    def get_queryset(self):
        return GradeRecord.objects.filter(diary__user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['has_school_diary'] = hasattr(self.request.user, 'schooldiary')
        return context

    def post(self, request, *args, **kwargs):
        form = GradeForm(request.POST)
        if form.is_valid():
            grade = form.save(commit=False)
            grade.diary = request.user.schooldiary
            grade.save()
            return redirect('school_diary')
        return self.get(request, *args, **kwargs)


class GradeCreateView(LoginRequiredMixin, CreateView):
    model = GradeRecord
    form_class = GradeForm
    template_name = 'diary/grade_form.html'
    success_url = reverse_lazy('school_diary')

    def form_valid(self, form):
        form.instance.diary = self.request.user.schooldiary
        return super().form_valid(form)

class GradeUpdateView(LoginRequiredMixin, OwnerRequiredMixin, UpdateView):
    model = GradeRecord
    form_class = GradeForm
    template_name = 'diary/grade_form.html'
    success_url = reverse_lazy('school_diary')

class GradeDeleteView(LoginRequiredMixin, OwnerRequiredMixin, DeleteView):
    model = GradeRecord
    template_name = 'diary/grade_confirm_delete.html'
    success_url = reverse_lazy('school_diary')