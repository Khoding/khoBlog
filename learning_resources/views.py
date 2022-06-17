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
        """Get all resources"""
        qs = Resource.objects.all()
        post = qs.first()
        serializer = ResourceSerializer(post)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        """Create a new resource"""
        serializer = ResourceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)


class ResourceViewSet(viewsets.ModelViewSet):
    """Viewset for resource"""

    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]

    def get_queryset(self):
        """Get queryset"""
        if self.request.user.is_superuser:
            queryset = Resource.objects.all()
        else:
            queryset = Resource.objects.filter(withdrawn=False)
        return queryset

    def get_serializer_class(self):
        """Get serializer class"""
        return ResourceSerializer


class ResourceCreateView(generics.CreateAPIView):
    """Viewset for resource"""

    permission_classes = (IsAdminUser,)

    def get_queryset(self):
        """Get queryset"""
        queryset = Resource.objects.all()
        return queryset

    def get_serializer_class(self):
        """Get serializer class"""
        return ResourceSerializer


class ResourceDetailView(generics.RetrieveAPIView):
    """Viewset for resource"""

    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]

    def get_queryset(self):
        """Get queryset"""
        if self.request.user.is_superuser:
            queryset = Resource.objects.all()
        else:
            queryset = Resource.objects.filter(withdrawn=False)
        return queryset

    def get_serializer_class(self):
        """Get serializer class"""
        return ResourceSerializer


class ResourceUpdateView(generics.UpdateAPIView):
    """Viewset for resource"""

    permission_classes = (IsAdminUser,)

    def get_queryset(self):
        """Get queryset"""
        queryset = Resource.objects.all()
        return queryset

    def get_serializer_class(self):
        """Get serializer class"""
        return ResourceSerializer


class ResourceDeleteView(generics.DestroyAPIView):
    """Viewset for resource"""

    permission_classes = (IsAdminUser,)

    def get_queryset(self):
        """Get queryset"""
        queryset = Resource.objects.all()
        return queryset

    def get_serializer_class(self):
        """Get serializer class"""
        return ResourceSerializer
