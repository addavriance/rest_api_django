from django.http import Http404
from rest_framework import mixins, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from ..exceptions import NotFoundError
from ..serializers import FlatsStatusSerializer, FlatsObjectSerializer, FlatsBulkSerializer
from ..models import Flats

from drf_yasg.utils import swagger_auto_schema


@swagger_auto_schema(
    method='PATCH',
    request_body=FlatsBulkSerializer,
    operation_id='flat_bulk_update',
    responses={
        204: 'Flats updated successfully',
        422: 'Invalid input data',
    },
)
@api_view(['PATCH'])
def bulk_update_flats(request):
    serializer = FlatsBulkSerializer(data=request.data)

    serializer.is_valid(raise_exception=True)

    validated_data = serializer.validated_data

    Flats.objects.filter(id__in=validated_data['flats']).update(
        size=validated_data['size'],
        rooms=validated_data['rooms'],
        price=validated_data['price']
    )

    return Response(status=204)


class FlatsViewSet(mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = Flats.objects.all()

    http_method_names = ['patch']

    def get_object(self):
        try:
            return super().get_object()
        except Http404:
            raise NotFoundError("Flat")

    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return FlatsStatusSerializer
        return FlatsObjectSerializer

    def update(self, request, pk=None, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=204)
