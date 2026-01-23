from django.urls import path
from . import views

urlpatterns = [
    path('', views.SessionListView.as_view(), name='session_list'),
    path('create/', views.SessionCreateView.as_view(), name='session_create'),
    path('<int:pk>/', views.SessionDetailView.as_view(), name='session_detail'),
]
