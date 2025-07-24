from django.urls import path
from .views import DiaryListView, DiaryCreateView, DiaryUpdateView, DiaryDeleteView, SchoolDiaryView, GradeCreateView, \
    GradeUpdateView, GradeDeleteView

urlpatterns = [
    # Основной дневник
    path('', DiaryListView.as_view(), name='diary_list'),
    path('create/', DiaryCreateView.as_view(), name='diary_create'),
    path('update/<int:pk>/', DiaryUpdateView.as_view(), name='diary_update'),
    path('delete/<int:pk>/', DiaryDeleteView.as_view(), name='diary_delete'),

    # Школьный дневник
    path('school/', SchoolDiaryView.as_view(), name='school_diary'),
    path('school/add/', GradeCreateView.as_view(), name='grade_create'),
    path('school/edit/<int:pk>/', GradeUpdateView.as_view(), name='grade_update'),
    path('school/delete/<int:pk>/', GradeDeleteView.as_view(), name='grade_delete'),
]
