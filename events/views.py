from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Event
from .serializers import EventSerializer
from alerts.models import Alert
from accounts.permissions import IsAdmin
from common.pagination import StandardResultsSetPagination

class EventAPIView(APIView):

    permission_classes = [IsAuthenticated]
    pagination_class = StandardResultsSetPagination

    def get(self, request):
        queryset = Event.objects.all().order_by('-created_at')

        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)

        serializer = EventSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    def post(self, request):
        if not IsAdmin().has_permission(request, self):
            return Response(
                {"detail": "Permission denied"},
                status=status.HTTP_403_FORBIDDEN
            )

        serializer = EventSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        event = serializer.save()

        # Auto-generate alert for High / Critical events
        if event.severity in ['High', 'Critical']:
            Alert.objects.create(event=event)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
