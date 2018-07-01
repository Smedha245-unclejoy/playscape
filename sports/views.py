from django.shortcuts import render
from rest_framework import generics
from rest_framework.views import APIView
from sports.models import Sport,SportFollower
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from sports.serializers import SportSerializer,SportFollowerSerializer
from rest_framework.permissions import IsAuthenticated

# Create your views here.


class SportView(APIView):
    permissions = [IsAuthenticated]
    def post(self, request, format='json'):
        serializer = SportSerializer(data=request.data)
        if serializer.is_valid():
            sport = serializer.save()
            if sport:
                json = serializer.data  #all user data
                return Response(json, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SportsFollowedByUser(generics.ListAPIView):
    permissions = [IsAuthenticated]
    serializer_class = SportFollowerSerializer
    def get_queryset(self):
        user_id = self.kwargs['user_id']
        queryset = SportFollower.objects.filter(follower=user_id)
        return queryset
class SportFollowerView(APIView):
    permissions = [IsAuthenticated]
    def post(self, request, format='json'):
        serializer = SportFollowerSerializer(data=request.data)
        if serializer.is_valid():
            sportFollow = serializer.save()
            if sportFollow:
                json = serializer.data
                return Response(json, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
