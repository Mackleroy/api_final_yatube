from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, generics, permissions, filters
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from api.permissions import ReadOnly
from api.serializers import *


class PostsViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated | ReadOnly]
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['text']
    filterset_fields = ['group']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def partial_update(self, request, *args, **kwargs):
        post = Post.objects.get(pk=kwargs['pk'])
        if request.user == post.author:
            self.update(request, *args, **kwargs)
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, *args, **kwargs):
        post = Post.objects.get(pk=kwargs['pk'])
        if request.user == post.author:
            post.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_403_FORBIDDEN)


class CommentList(viewsets.ViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['text']

    def list(self, request, **kwargs):
        queryset = Comment.objects.filter(post=kwargs.get('post_id'))
        serializer = CommentSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, **kwargs):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user,
                            post=Post.objects.get(pk=kwargs.get('post_id')))
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)


class CommentDetail(viewsets.ViewSet):

    def retrieve(self, request, **kwargs):
        comment = get_object_or_404(Comment, pk=kwargs.get('comment_id'),
                                    post=kwargs.get('post_id'))
        serializer = CommentSerializer(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, **kwargs):
        comment = get_object_or_404(Comment, pk=kwargs.get('comment_id'),
                                    post=kwargs.get('post_id'))
        serializer = CommentSerializer(comment, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

    def partial_update(self, request, **kwargs):
        comment = get_object_or_404(Comment, pk=kwargs.get('comment_id'),
                                    post=kwargs.get('post_id'))
        if request.user == comment.author:
            serializer = CommentSerializer(comment, data=request.data,
                                           partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, **kwargs):
        comment = get_object_or_404(Comment, pk=kwargs.get('comment_id'),
                                    post=kwargs.get('post_id'))
        if request.user == comment.author:
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_403_FORBIDDEN)


class FollowListCreate(generics.ListCreateAPIView):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [permissions.IsAuthenticated | ReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['=user__username', '=following__username']

    def create(self, request, **kwargs):
        serializer = FollowSerializer(data=request.data)
        if bool(request.data):
            following = User.objects.get(username=request.data['following'])
            follow = Follow.objects.filter(user=request.user,
                                           following=following)
            if not follow.exists() and serializer.is_valid():
                serializer.save(user=request.user, following=following)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class GroupListCreate(generics.ListCreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated | ReadOnly]

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)
