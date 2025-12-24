from django.urls import path

# Tools App APIs
from .views import EventCreateAPIView

urlpatterns = [
    path('', EventCreateAPIView.as_view(), name='event-create'),]
