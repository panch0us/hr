from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.MainView.as_view()),
    path('filter_analitics/', views.FilterAnalyticsView.as_view()),
    path('analytics/', views.AnalyticsView.as_view()),
    path('service/<slug:slug>/', views.ServicesDetailView.as_view(), name='services_detail'),
    path('department/<slug:slug>/', views.DepartmentsDetailView.as_view(), name='departments_detail'),
    path('candidate/<slug:slug>/', views.CandidatesDetailView.as_view(), name='candidates_detail'),
    path('division_personnel/<slug:slug>/', views.DivisionsPersonnelDetailView.as_view(), name='divisions_personnel_detail'),
]