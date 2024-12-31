from django.http import Http404
from rest_framework import mixins, viewsets
from rest_framework.response import Response

from ..exceptions import NotFoundError
from ..serializers import SectionsInitSerializer, SectionsObjectSerializer
from ..models import Sections, Flats


class SectionsViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Sections.objects.all()

    http_method_names = ['post', 'get']

    def get_object(self):
        try:
            return super().get_object()
        except Http404:
            raise NotFoundError("Section")

    def get_serializer_class(self):
        if self.action == "create":
            return SectionsInitSerializer
        return SectionsObjectSerializer

    def retrieve(self, request, pk=None, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        return Response({'data': serializer.data})

    def create(self, request, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        instance = self.perform_create(serializer)
        return Response({'data': {'id': instance.id}}, status=201)

    def perform_create(self, serializer):
        section = serializer.save()

        flat_number = section.starting_flat_number
        flat_list = []

        for floor in range(1, section.floors + 1):
            for _ in range(section.flats_on_floor):
                flat_list.append(Flats(
                    section=section,
                    floor=floor,
                    flat_number=flat_number,
                    status='free'
                ))
                flat_number += 1

        Flats.objects.bulk_create(flat_list)

        return section
