from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from posts.serializers import PostSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework import generics
from rest_framework.views import APIView
from posts.models import Post,PostImage
from rest_framework import status
from friends.models import Friendship
from django.db.models import Q
from rest_framework.decorators import parser_classes
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
# Create your views here.


@parser_classes((MultiPartParser,))
class Upload(APIView):
    """
    To create a new post including multiple images
    """
    permissions = [IsAuthenticated]
    parser_classes = MultiPartParser
    serializer_class = PostSerializer

    def post(self,request):
        request.data['user_id']=self.request.user.id
        serializer = PostSerializer(data = request.data)
        if serializer.is_valid():
            post=serializer.save()
            if post:
                json = serializer.data
                return Response(json,status=status.HTTP_201_CREATED)
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class AllPosts(generics.ListAPIView):
    """
    To fetch all posts created by the user when he makes a request by himself using his user_id
    """
    permissions = [IsAuthenticated]
    serializer_class = PostSerializer
    def get_queryset(self):
        user_id = self.kwargs['user_id']
        queryset = Post.objects.filter(user_id=user_id,is_active=True)
        return queryset

class PostDetail(APIView):
    """
    Detail view of a particular post created by the user
    """
    permissions = [IsAuthenticated]
    def get(self,request, post_id):
        """
        View individual post
        """
        id = self.kwargs['post_id']
        post = get_object_or_404(Post, pk=post_id)
         #pk is primary key for post table
        return Response(PostSerializer(post).data)

class PostFeed(generics.ListAPIView):
    """
    PostFeed first select * from posts where post.author=friend of user
    """
    permissions = [IsAuthenticated]
    serializer_class = PostSerializer
    def get_queryset(self):
        author = get_object_or_404(Friendship,Q(creator=self.request.user.id)|Q(friend=self.request.user.id))
        for author_in in author:
            queryset = Post.objects.filter(is_active=True,user_id=author.entry_set.all()|author.creator.entry_set.all())
        return queryset
