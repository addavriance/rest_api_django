from django.http import Http404
from rest_framework import mixins, viewsets
from rest_framework.response import Response
from rest_framework.serializers import ValidationError as DRFValidationError

from ..exceptions import NotFoundError, ValidationError
from ..serializers import ProjectsListSerializer, ProjectsObjectSerializer
from ..models import Projects


class ProjectsViewSet(mixins.ListModelMixin, mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                      mixins.UpdateModelMixin, viewsets.GenericViewSet):

    queryset = Projects.objects.all()

    http_method_names = ['post', 'get', 'patch']

    def get_object(self):
        try:
            return super().get_object()
        except Http404:
            raise NotFoundError("Project")

    def get_serializer_class(self):
        if self.action == 'list':
            return ProjectsListSerializer
        return ProjectsObjectSerializer

    def list(self, request, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response({'data': {'projects': serializer.data}})

    def retrieve(self, request, pk=None, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)

        return Response({'data': serializer.data})

    def create(self, request, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except DRFValidationError as e:
            raise ValidationError(e.detail)

        instance = serializer.save()
        return Response({'data': {'id': instance.id}}, status=201)

    def update(self, request, pk=None, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(status=204)