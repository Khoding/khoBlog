# third party imports
from rest_framework import generics, viewsets
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Resource
from .serializers import ResourceSerializer


class TestView(APIView):

    permission_classes = (IsAdminUser, )

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
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer


class ResourceCreateView(generics.CreateAPIView):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer
    permission_classes = (IsAdminUser, )


class ResourceDetailView(generics.RetrieveAPIView):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer
    permission_classes = (IsAdminUser, )


class ResourceUpdateView(generics.UpdateAPIView):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer
    permission_classes = (IsAdminUser, )


class ResourceDeleteView(generics.DestroyAPIView):
    queryset = Resource.objects.all()
    serializer_class = ResourceSerializer
    permission_classes = (IsAdminUser, )
