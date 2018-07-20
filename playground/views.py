from django.shortcuts import render
from rest_framework.views import APIView
from playground.models import Playground
from .serializers import PlaygroundSerializer
from rest_framework import generics
from .serializers import PlaygroundSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
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
