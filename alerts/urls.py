from django.urls import path
from .views import AlertListAPIView, AlertUpdateAPIView

urlpatterns = [
    path('', AlertListAPIView.as_view(), name='alert-list'),
    path('<int:pk>/', AlertUpdateAPIView.as_view(), name='alert-update'),
]