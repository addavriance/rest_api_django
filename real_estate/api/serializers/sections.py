from rest_framework import serializers

from ..models import Sections, Flats, Houses
from .flats import FlatsObjectSerializer


class SectionsInitSerializer(serializers.ModelSerializer):
    house_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Houses.objects.all(), source='house')

    class Meta:
        model = Sections
        fields = ['id', 'house_id', 'number',
                  'floors', 'flats_on_floor',
                  'starting_flat_number']

    @staticmethod
    def validate_floors(value):
        if not isinstance(value, int):
            raise serializers.ValidationError("Floors must be a number")
        return value

    @staticmethod
    def validate_flats_on_floor(value):
        if not isinstance(value, int):
            raise serializers.ValidationError("Flats on floor must be a number")
        return value

    @staticmethod
    def validate_starting_flat_number(value):
        if not isinstance(value, int):
            raise serializers.ValidationError("Starting flat number must be a number")
        return value


class SectionsObjectSerializer(serializers.ModelSerializer):
    flats = serializers.SerializerMethodField()

    class Meta:
        model = Sections
        fields = ['id', 'number', 'flats']

    @staticmethod
    def get_flats(obj):
        flats = Flats.objects.filter(section=obj)
        return FlatsObjectSerializer(flats, many=True).data
