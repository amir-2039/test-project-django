from rest_framework import serializers
from consumers.models import Consumer


class ConsumerSerializer(serializers.ModelSerializer):
    geometry = serializers.SerializerMethodField()
    properties = serializers.SerializerMethodField()

    class Meta:
        model = Consumer
        fields = ('geometry', 'properties')

    def get_geometry(self, obj):
        return {
            'type': 'Point',
            'coordinates': [float(obj.longitude), float(obj.latitude)]
        }

    def get_properties(self, obj):
        return {
            'id': obj.id,
            'amount_due': float(obj.amount_due),
            'previous_jobs_count': int(obj.previous_jobs_count),
            'status': obj.status,
            'street': obj.street
        }


class GeoJSONSerializer(serializers.Serializer):
    type = serializers.CharField(max_length=100, default='FeatureCollection')
    features = ConsumerSerializer(many=True)
