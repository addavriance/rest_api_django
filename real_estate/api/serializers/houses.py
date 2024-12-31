from rest_framework import serializers

from ..constants import BUILT_YEAR_RANGE, BUILT_QUARTER_RANGE
from ..models import Houses, Sections, Projects
from ..utils import in_range


class HousesInitSerializer(serializers.ModelSerializer):
    project_id = serializers.PrimaryKeyRelatedField(write_only=True, queryset=Projects.objects.all(), source='project')

    class Meta:
        model = Houses
        fields = ['id', 'project_id', 'name', 'address', 'built_year', 'built_quarter']

    @staticmethod
    def validate_built_year(value):
        if not isinstance(value, int) or not in_range(value, BUILT_YEAR_RANGE):
            raise serializers.ValidationError("Built year must be a number between 800 and 2050")
        return value

    @staticmethod
    def validate_built_quarter(value):
        if not isinstance(value, int) or not in_range(value, BUILT_QUARTER_RANGE):
            raise serializers.ValidationError("Built quarter must be a number between 1 and 4")
        return value


class HousesObjectSerializer(serializers.ModelSerializer):
    sections = serializers.SerializerMethodField()

    class Meta:
        model = Houses
        fields = ['id', 'name', 'address', 'built_year', 'built_quarter', 'sections']

    @staticmethod
    def get_sections(obj):
        sections = Sections.objects.filter(house=obj)
        return [{"id": section.id, "number": section.number} for section in sections]