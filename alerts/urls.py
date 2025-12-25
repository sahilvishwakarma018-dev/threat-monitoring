from django.urls import path
from .views import AlertAPIView

urlpatterns = [
    path('', AlertAPIView.as_view(), name='alert-list'),
    path('<int:pk>/', AlertAPIView.as_view(), name='alert-update'),
]