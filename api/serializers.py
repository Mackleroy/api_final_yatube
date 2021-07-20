from rest_framework import serializers

from .models import Post, Comment, Follow, Group, User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id', 'username']
        model = User


class PostSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        fields = ['id', 'text', 'author', 'pub_date']
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        fields = ['id', 'author', 'post', 'text', 'created']
        read_only_fields = ['author', 'post', 'created']
        model = Comment


class FollowSerializer(serializers.ModelSerializer):
    # user = UserSerializer(read_only=True)
    # following = UserSerializer(read_only=True)
    user = serializers.ReadOnlyField(source='user.username')
    following = serializers.ReadOnlyField(source='following.username')

    class Meta:
        fields = ['user', 'following']
        read_only_fields = ['user', 'following']
        model = Follow


class GroupSerializer(serializers.ModelSerializer):
    creator = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        fields = ['id', 'title', 'description', 'creator']
        model = Group
