from rest_framework import serializers

from ..constants import FLAT_STATUSES
from ..models import Sections, Flats


class FlatsBulkSerializer(serializers.Serializer):
    flats = serializers.ListField(
        child=serializers.IntegerField(),
        required=True
    )
    size = serializers.FloatField(
        required=True
    )
    rooms = serializers.IntegerField(
        required=True,
        min_value=0,
        max_value=6,
    )
    price = serializers.IntegerField(
        required=True,
        min_value=0,
    )

    @staticmethod
    def validate_flats(value):
        existing_flats = set(Flats.objects.filter(
            id__in=value
        ).values_list('id', flat=True))

        non_existing = set(value) - existing_flats
        if non_existing:
            raise serializers.ValidationError(f'Flats with ids {list(non_existing)} do not exist')
        return value


class FlatsStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = Flats
        fields = ['status']

    @staticmethod
    def validate_status(value):
        if value not in FLAT_STATUSES:
            raise serializers.ValidationError("Status must be one of: free, reserved, sold")
        return value


class FlatsObjectSerializer(serializers.ModelSerializer):
    section = serializers.SerializerMethodField()

    class Meta:
        model = Flats
        fields = ['id', 'floor','flat_number', 'status',
                  'price', 'size', 'rooms', 'section']

    @staticmethod
    def get_section(obj):
        section = Sections.objects.get(id=obj.section_id)
        return {"id": section.id, "number": section.number, "floors": section.floors, "flats_on_floor": section.flats_on_floor}
