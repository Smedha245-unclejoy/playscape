from django.shortcuts import render
from rest_framework.views import APIView
from playground.models import Playground
from .serializers import PlaygroundSerializer
from rest_framework import generics
from .serializers import PlaygroundSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from rest_framework import status
# Create your views here.

class PlaygroundView(APIView):
    permissions = [IsAuthenticated]
    def post(self,request,format='json'):
        request.data['creator']=request.user.id
        serializer = PlaygroundSerializer(data=request.data)
        if serializer.is_valid():
            playground = serializer.save()
            if playground:
                json = serializer.data
                return Response(json,status=status.HTTP_201_CREATED)

        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class AllPlaygroundList(generics.ListAPIView):
    permissions = [IsAuthenticated]
    serializer_class = PlaygroundSerializer
    def get_queryset(self):
        queryset = Playground.objects.all()
        return queryset

class UpdatePlayground(generics.UpdateAPIView):
    permissions = [IsAuthenticated]
    serializer_class = PlaygroundSerializer
    queryset = Playground.objects.all()
    lookup_field = 'id'

    def post(self, request, *args, **kwargs):
        instance=Playground.objects.filter(id=request.data['id'])
        if instance:
            serializer = PlaygroundSerializer(instance=instance,data=request.data)
            if serializer.is_valid():
                serializer.save(instance=instance,validated_data=serializer.validated_data)

                return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
