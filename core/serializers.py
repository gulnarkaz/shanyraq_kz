from rest_framework import serializers
from .models import Shanyrak, Comment

class ShanyrakCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shanyrak
        fields = ('type', 'price', 'address', 'area', 'rooms_count', 'description')

    def create(self, validated_data):
        user = self.context['request'].user
        shanyrak = Shanyrak.objects.create(user=user, **validated_data)
        return shanyrak

class ShanyrakDetailSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='user.id', read_only=True)
    total_comments = serializers.SerializerMethodField()  

    class Meta:
        model = Shanyrak
        fields = ('id', 'type', 'price', 'address', 'area', 'rooms_count', 'description', 'user_id', 'total_comments')
        read_only_fields = ('id', 'user_id', 'total_comments')

    def get_total_comments(self, obj):
        """Возвращает общее количество комментариев для данного объявления."""
        return obj.comments.count()

class ShanyrakIdResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()

class CommentSerializer(serializers.ModelSerializer):
    author_id = serializers.IntegerField(source='author.id', read_only=True)
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Comment
        fields = ('id', 'content', 'created_at', 'author_id')
        read_only_fields = ('id', 'created_at', 'author_id')
        
class FavoriteShanyrakSerializer(serializers.ModelSerializer):
    _id = serializers.IntegerField(source='id')
    address = serializers.CharField()

    class Meta:
        model = Shanyrak
        fields = ('_id', 'address')