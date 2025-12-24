from rest_framework import serializers
from .models import Alert
from events.serializers import EventSerializer

class AlertSerializer(serializers.ModelSerializer):
    event = EventSerializer(read_only=True)

    class Meta:
        model = Alert
        fields = '__all__'
