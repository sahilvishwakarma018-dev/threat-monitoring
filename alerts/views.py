from rest_framework.generics import ListAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from .models import Alert
from .serializers import AlertSerializer
from accounts.permissions import IsAdmin

import logging
logger = logging.getLogger(__name__)

class AlertListAPIView(ListAPIView):
    serializer_class = AlertSerializer
    # permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = Alert.objects.select_related('event')

        severity = self.request.query_params.get('severity')
        status = self.request.query_params.get('status')

        if severity:
            queryset = queryset.filter(event__severity=severity)

        if status:
            queryset = queryset.filter(status=status)

        return queryset



class AlertUpdateAPIView(UpdateAPIView):
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer
    permission_classes = [IsAuthenticated, IsAdmin]

    def perform_update(self, serializer):
        alert = serializer.save()
        logger.info(
            f"Alert {alert.id} updated to {alert.status} by user {self.request.user.username}"
        )
