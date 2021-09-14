# third party imports
from rest_framework import generics, viewsets
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Resource
from .serializers import ResourceSerializer


class TestView(APIView):
    permission_classes = (IsAdminUser,)

    @staticmethod
    def get(request, *args, **kwargs):
        qs = Resource.objects.all()
        post = qs.first()
        serializer = ResourceSerializer(post)
        return Response(serializer.data)

    @staticmethod
    def post(request, *args, **kwargs):
        serializer = ResourceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


class ResourceViewSet(viewsets.ModelViewSet):
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]

    def get_queryset(self):
        if self.request.user.is_superuser:
            queryset = Resource.objects.all()
        else:
            queryset = Resource.objects.filter(withdrawn=False)
        return queryset

    def get_serializer_class(self):
        if self.request.version == 'v2':
            return ResourceSerializer
        return ResourceSerializer


class ResourceCreateView(generics.CreateAPIView):
    permission_classes = (IsAdminUser,)

    def get_queryset(self):
        queryset = Resource.objects.all()
        return queryset

    def get_serializer_class(self):
        if self.request.version == 'v2':
            return ResourceSerializer
        return ResourceSerializer


class ResourceDetailView(generics.RetrieveAPIView):
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]

    def get_queryset(self):
        if self.request.user.is_superuser:
            queryset = Resource.objects.all()
        else:
            queryset = Resource.objects.filter(withdrawn=False)
        return queryset

    def get_serializer_class(self):
        if self.request.version == 'v2':
            return ResourceSerializer
        return ResourceSerializer


class ResourceUpdateView(generics.UpdateAPIView):
    permission_classes = (IsAdminUser,)

    def get_queryset(self):
        queryset = Resource.objects.all()
        return queryset

    def get_serializer_class(self):
        if self.request.version == 'v2':
            return ResourceSerializer
        return ResourceSerializer


class ResourceDeleteView(generics.DestroyAPIView):
    permission_classes = (IsAdminUser,)

    def get_queryset(self):
        queryset = Resource.objects.all()
        return queryset

    def get_serializer_class(self):
        if self.request.version == 'v2':
            return ResourceSerializer
        return ResourceSerializer
