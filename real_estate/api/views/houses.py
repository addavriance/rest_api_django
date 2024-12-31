from django.http import Http404
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from ..exceptions import NotFoundError
from ..serializers import HousesInitSerializer, HousesObjectSerializer, FlatsObjectSerializer
from ..models import Houses, Flats


class HousesViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                    mixins.UpdateModelMixin, viewsets.GenericViewSet):
    queryset = Houses.objects.all()

    http_method_names = ['post', 'get', 'patch']

    def get_object(self):
        try:
            return super().get_object()
        except Http404:
            raise NotFoundError("House")

    def get_serializer_class(self):
        if self.action == "create":
            return HousesInitSerializer
        return HousesObjectSerializer

    def retrieve(self, request, pk=None, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        return Response({'data': serializer.data})

    def create(self, request, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        instance = serializer.save()
        return Response({'data': {'id': instance.id}}, status=201)

    def update(self, request, pk=None, **kwargs):
        instance = self.get_object()

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(status=204)

    @action(detail=True, methods=['get'], url_path='flats')
    def house_flats(self, request, pk=None):
        house = self.get_object()

        flats = Flats.objects.filter(section__house=house)
        serializer = FlatsObjectSerializer(flats, many=True)

        return Response({
            'data': {
                'flats': serializer.data
            }
        })
