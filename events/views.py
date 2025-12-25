from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Event
from .serializers import EventSerializer
from alerts.models import Alert
from accounts.permissions import IsAdmin


class EventAPIView(APIView):

    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request):
        serializer = EventSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        event = serializer.save()

        # Auto-generate alert for High / Critical events
        if event.severity in ['High', 'Critical']:
            Alert.objects.create(event=event)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
