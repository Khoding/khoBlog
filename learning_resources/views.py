# third party imports
from rest_framework import generics, viewsets
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Resource
from .serializers import ResourceSerializer


class TestView(APIView):
    """Test api view"""

    permission_classes = (IsAdminUser,)

    def get(self, request, *args, **kwargs):
        qs = Resource.objects.all()
        post = qs.first()
        serializer = ResourceSerializer(post)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = ResourceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


class ResourceViewSet(viewsets.ModelViewSet):
    """Viewset for resource"""

    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]

    def get_queryset(self):
        if self.request.user.is_superuser:
            queryset = Resource.objects.all()
        else:
            queryset = Resource.objects.filter(withdrawn=False)
        return queryset

    def get_serializer_class(self):
        return ResourceSerializer


class ResourceCreateView(generics.CreateAPIView):
    """Viewset for resource"""

    permission_classes = (IsAdminUser,)

    def get_queryset(self):
        queryset = Resource.objects.all()
        return queryset

    def get_serializer_class(self):
        return ResourceSerializer


class ResourceDetailView(generics.RetrieveAPIView):
    """Viewset for resource"""

    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]

    def get_queryset(self):
        if self.request.user.is_superuser:
            queryset = Resource.objects.all()
        else:
            queryset = Resource.objects.filter(withdrawn=False)
        return queryset

    def get_serializer_class(self):
        return ResourceSerializer


class ResourceUpdateView(generics.UpdateAPIView):
    permission_classes = (IsAdminUser,)

    def get_queryset(self):
        queryset = Resource.objects.all()
        return queryset

    def get_serializer_class(self):
        return ResourceSerializer


class ResourceDeleteView(generics.DestroyAPIView):
    permission_classes = (IsAdminUser,)

    def get_queryset(self):
        queryset = Resource.objects.all()
        return queryset

    def get_serializer_class(self):
        return ResourceSerializer
