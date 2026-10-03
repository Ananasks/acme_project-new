# Маршруты приложения birthday.
# Подключение приложений и выдача media находятся в acme_project/urls.py.
from django.urls import path

from . import views

app_name = 'birthday'

urlpatterns = [
    path('login_only/', views.simple_view),
    path('create/', views.BirthdayCreateView.as_view(), name='create'),
    path('list/', views.BirthdayListView.as_view(), name='list'),
    path('<int:pk>/', views.BirthdayDetailView.as_view(), name='detail'),
    path(
        '<int:pk>/edit/',
        views.BirthdayUpdateView.as_view(),
        name='edit',
    ),
    path('<int:pk>/delete/', views.BirthdayDeleteView.as_view(), name='delete'),
]
