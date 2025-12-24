from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from .models import Event
from .serializers import EventSerializer
from alerts.models import Alert
from accounts.permissions import IsAdmin

class EventCreateAPIView(CreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

    def perform_create(self, serializer):
        event = serializer.save()

        # Auto-generate alert for High / Critical events
        if event.severity in ['High', 'Critical']:
            Alert.objects.create(event=event)
