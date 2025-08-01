from django.urls import path
from .views import DiaryListView, DiaryCreateView, DiaryUpdateView, DiaryDeleteView, DiaryDetailView

urlpatterns = [
    # Основной дневник
    path('', DiaryListView.as_view(), name='diary_list'),
    path('create/', DiaryCreateView.as_view(), name='diary_create'),
    path('detail/<int:pk>/', DiaryDetailView.as_view(), name='diary_detail'),
    path('update/<int:pk>/', DiaryUpdateView.as_view(), name='diary_update'),
    path('delete/<int:pk>/', DiaryDeleteView.as_view(), name='diary_delete'),

]
