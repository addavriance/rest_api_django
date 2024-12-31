from rest_framework import serializers

from ..models import Projects, Flats, Houses


class ProjectsListSerializer(serializers.ModelSerializer):
    flat_statuses = serializers.SerializerMethodField()

    class Meta:
        model = Projects
        fields = ['id', 'name', 'flat_statuses']

    @staticmethod
    def get_flat_statuses(obj):

        flats = Flats.objects.filter(section__house__project=obj)

        return {
            'free': flats.filter(status='free').count(),
            'reserved': flats.filter(status='reserved').count(),
            'sold': flats.filter(status='sold').count(),
        }


class ProjectsObjectSerializer(serializers.ModelSerializer):
    houses = serializers.SerializerMethodField()

    class Meta:
        model = Projects
        fields = ['id', 'name', 'coords', 'district', 'website', 'houses']

    @staticmethod
    def get_houses(obj):
        houses = Houses.objects.filter(project=obj)

        return [{"id": house.id, "name": house.name} for house in houses]

    @staticmethod
    def validate_coords(value):
        try:
            _lat, _lon = map(float, value.split(','))
            return value
        except Exception:
            raise serializers.ValidationError("Coordinates must be two numbers separated by comma")

    @staticmethod
    def validate_website(value):
        if not value.startswith(('http://', 'https://')):
            raise serializers.ValidationError("Website must start with http:// or https://")
        return value
