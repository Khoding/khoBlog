# third party imports
from rest_framework import generics, viewsets
from rest_framework.permissions import DjangoModelPermissionsOrAnonReadOnly, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Resource
from .serializers import ResourceSerializer


class TestView(APIView):
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
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    serializer_class = ResourceSerializer

    def get_queryset(self):
        queryset = Resource.objects.filter(withdrawn=False)
        return queryset


class ResourceCreateView(generics.CreateAPIView):
    serializer_class = ResourceSerializer
    permission_classes = (IsAdminUser,)

    def get_queryset(self):
        queryset = Resource.objects.all()
        return queryset


class ResourceDetailView(generics.RetrieveAPIView):
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    serializer_class = ResourceSerializer

    def get_queryset(self):
        queryset = Resource.objects.filter(withdrawn=False)
        return queryset


class ResourceUpdateView(generics.UpdateAPIView):
    serializer_class = ResourceSerializer
    permission_classes = (IsAdminUser,)

    def get_queryset(self):
        queryset = Resource.objects.all()
        return queryset


class ResourceDeleteView(generics.DestroyAPIView):
    serializer_class = ResourceSerializer
    permission_classes = (IsAdminUser,)

    def get_queryset(self):
        queryset = Resource.objects.all()
        return queryset
