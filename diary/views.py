from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

from diary.forms import DiaryEntryForm
from diary.mixins import OwnerRequiredMixin
from diary.models import DiaryEntry, FileAttachment


def form_valid(self, form):
    entry = form.save(commit=False)
    entry.user = self.request.user
    entry.save()
    form.save_m2m()  # Для тегов

    # Обработка файлов
    files = self.request.FILES.getlist('attachments')
    for f in files:
        attachment = FileAttachment.objects.create(file=f)
        entry.files.add(attachment)

    return super().form_valid(form)


def home(request):
    if request.user.is_authenticated:
        diary_entries = DiaryEntry.objects.filter(user=request.user).order_by('-date')[:5]
        return render(request, 'diary/home.html', {'diary_entries': diary_entries})
    return render(request, 'diary/home.html')


def diary_list(request):
    search_query = request.GET.get('search', '')

    if search_query:
        entries = DiaryEntry.objects.filter(
            Q(user=request.user) &
            (Q(title__icontains=search_query) |
             Q(text__icontains=search_query)))
    else:
        entries = DiaryEntry.objects.filter(user=request.user)

    paginator = Paginator(entries, 10)  # 10 записей на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'diary/diary_list.html', {
        'page_obj': page_obj,
        'search_query': search_query
    })


# Основной дневник
class DiaryListView(LoginRequiredMixin, ListView):
    model = DiaryEntry
    template_name = 'diary/diary_list.html'
    context_object_name = 'entries'
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset().filter(user=self.request.user)
        search_query = self.request.GET.get('search', '')

        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(text__icontains=search_query))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        return context


class DiaryDetailView(LoginRequiredMixin, OwnerRequiredMixin, DetailView):
    model = DiaryEntry
    template_name = 'diary/diary_detail.html'
    context_object_name = 'entry'

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
    form_class = DiaryEntryForm
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
