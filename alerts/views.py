from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Alert
from .serializers import AlertSerializer
from accounts.permissions import IsAdmin

import logging
logger = logging.getLogger(__name__)


class AlertAPIView(APIView):
    """
    GET    -> List alerts with filters
    PATCH  -> Update alert status (Admin only)
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        queryset = Alert.objects.select_related('event')

        severity = request.query_params.get('severity')
        status_param = request.query_params.get('status')

        if severity:
            queryset = queryset.filter(event__severity=severity)

        if status_param:
            queryset = queryset.filter(status=status_param)

        serializer = AlertSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        if not IsAdmin().has_permission(request, self):
            return Response(
                {"detail": "You do not have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN
            )

        try:
            alert = Alert.objects.get(pk=pk)
        except Alert.DoesNotExist:
            return Response(
                {"detail": "Alert not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = AlertSerializer(alert, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        alert = serializer.save()

        logger.info(
            f"Alert {alert.id} updated to {alert.status} by user {request.user.username}"
        )

        return Response(serializer.data, status=status.HTTP_200_OK)
