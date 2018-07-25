from django.shortcuts import render,get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from .serializers import FriendSerializer
from .models import Friendship
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

class RequestFriendship(APIView):
    permissions=[IsAuthenticated]
    serializer_class = FriendSerializer
    def post(self,request,format='json'):
        request.data['creator'] = self.request.user.id
        serializer = FriendSerializer(data=request.data)
        if serializer.is_valid():
            friendship = serializer.save()
            if friendship:
                json = serializer.data
                return Response(json,status=status.HTTP_201_CREATED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class AcceptFriendship(generics.UpdateAPIView):
    permissions = [IsAuthenticated]
    serializer_class = FriendSerializer
    queryset = Friendship.objects.all()
    lookup_field = 'id'
    def post(self, request, *args, **kwargs):
        instance=Friendship.objects.filter(id=request.data['id'])
        if instance:
            serializer = FriendSerializer(instance=instance,data=request.data)
            if serializer.is_valid():
                serializer.save(instance=instance,validated_data=serializer.validated_data)
                return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
