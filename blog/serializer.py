from rest_framework import serializers, viewsets
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Comment, Post
from rest_framework.decorators import action
from rest_framework.response import Response
from core.views import ActionSerializedViewSet



class CommentSerializer(serializers.ModelSerializer):
    #text = serializers.CharField(max_length=200)
    #created_date = serializers.DateTimeField()
    class Meta:
        model = Comment
        fields = '__all__'


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    @action(detail=True, methods=['POST'], permission_classes=[IsAuthenticated])
    def publish(self, request, pk=None):
        post = self.get_object()
        post.publish()
        return Response({'status': 'published'})
    

class BlogPostListSerializer(serializers.ModelSerializer):
    #preview_text = serializers.SerializerMethodField()

    def get_preview_text(self, post):
        return post.get_text_preview()
    
    class Meta:
        model = Post
        fields = '__all__'


class BlogPostViewSet(viewsets.ModelViewSet):
    serializer_class = BlogPostListSerializer
    queryset = Post.objects.all()


class BlogPostCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        exclude = ()

class BlogPostDetailSerializer(serializers.ModelSerializer):
    comments_count = serializers.SerializerMethodField()
    comments = CommentSerializer(many=True, read_only=True)

    def get_comments_count(self, obj):
        return obj.comments.count()
    
    class Meta:
        model = Post
        fields = '__all__'


class BlogPostViewSet(ActionSerializedViewSet):
    serializer_class = BlogPostListSerializer
    queryset = Post.objects.all()

    action_serializers = {
        'list' : BlogPostListSerializer,
        'retrieve' : BlogPostDetailSerializer,
        'create' : BlogPostCreateUpdateSerializer,
        'update' : BlogPostCreateUpdateSerializer
    }

    def get_queryset(self):
        queryset = self.queryset
        author = self.request.query_params.get('author', None)
        if author:
            queryset = queryset.filter(author__username=author)
        return queryset



    @action(detail=True, methods=['POST'], permission_classes=[IsAuthenticated])
    def publish(self, request, pk=None):
        post = self.get_object()
        if request.user == post.author:
            return Response({
                'message' : 'blog post was published'
            }, status=status.HTTP_200_OK)
        
        return Response({
            'error' : 'You do not have permissions',
        }, status=status.HTTP_403_FORBIDDEN)
        

    @action(detail=False)
    def published_posts(self, request):
        published_posts = Post.published.all()
        page = self.paginate_queryset(published_posts)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(published_posts, nany=True)
        return Response(serializer.data)
            


   