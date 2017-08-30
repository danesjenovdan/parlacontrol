from dashboard.models import Status

from rest_framework import serializers
from datetime import datetime

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ('status_type', 'status_note', 'status_done', 'update_time')

    def update(self, instance, validated_data):
        instance.status_type = validated_data.get('status_type', instance.status_type)
        instance.status_note = validated_data.get('status_note', instance.status_note)
        instance.status_done = validated_data.get('status_done', instance.status_done)
        instance.update_time = datetime.now()
        instance.save()
        return instance