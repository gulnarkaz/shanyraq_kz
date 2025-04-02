from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Q

from .models import Shanyrak, Comment
from .serializers import (
    ShanyrakCreateSerializer,
    ShanyrakDetailSerializer,
    ShanyrakIdResponseSerializer,
    CommentSerializer,
    ShanyrakListSerializer
)
from rest_framework.pagination import LimitOffsetPagination

class ShanyrakCreateView(generics.CreateAPIView):
    queryset = Shanyrak.objects.all()
    serializer_class = ShanyrakCreateSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        print(f"Authenticated user: {request.user}")
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        instance = serializer.save()
        response_serializer = ShanyrakIdResponseSerializer(data={'id': instance.id})
        response_serializer.is_valid(raise_exception=True)
        return Response(response_serializer.data, status=status.HTTP_200_OK)

class ShanyrakDetailView(generics.RetrieveAPIView):
    queryset = Shanyrak.objects.all()
    serializer_class = ShanyrakDetailSerializer
    permission_classes = (AllowAny,)
    lookup_field = 'id'

class ShanyrakUpdateView(generics.UpdateAPIView):
    serializer_class = ShanyrakCreateSerializer 
    permission_classes = (IsAuthenticated,)
    lookup_field = 'id'

    def get_queryset(self):
        return Shanyrak.objects.filter(user=self.request.user)

class ShanyrakDeleteView(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    lookup_field = 'id'

    def get_queryset(self):
        return Shanyrak.objects.filter(user=self.request.user)

class CommentCreateView(generics.CreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        shanyrak_id = self.kwargs.get('shanyrak_id')
        shanyrak = get_object_or_404(Shanyrak, id=shanyrak_id)
        serializer.save(shanyrak=shanyrak, author=self.request.user)

class CommentListView(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = (AllowAny,)

    def get_queryset(self):
        shanyrak_id = self.kwargs.get('shanyrak_id')
        return Comment.objects.filter(shanyrak_id=shanyrak_id).order_by('-created_at')

class CommentUpdateView(generics.UpdateAPIView):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated,)
    lookup_field = 'comment_id'

    def get_queryset(self):
        shanyrak_id = self.kwargs.get('shanyrak_id')
        return Comment.objects.filter(shanyrak_id=shanyrak_id, author=self.request.user)

class CommentDeleteView(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    lookup_field = 'comment_id'

    def get_queryset(self):
        shanyrak_id = self.kwargs.get('shanyrak_id')
        comment_id = self.kwargs.get('comment_id')
        comment = get_object_or_404(Comment, id=comment_id, shanyrak_id=shanyrak_id)
        shanyrak = get_object_or_404(Shanyrak, id=shanyrak_id, user=self.request.user)
        return Comment.objects.filter(id=comment_id, shanyrak_id=shanyrak_id)
    
class ShanyrakPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 100

class ShanyrakListView(generics.ListAPIView):
    serializer_class = ShanyrakListSerializer
    pagination_class = ShanyrakPagination

    def get_queryset(self):
        queryset = Shanyrak.objects.all().order_by('-created_at')

        # Фильтрация по параметрам запроса
        type_param = self.request.query_params.get('type')
        rooms_count_param = self.request.query_params.get('rooms_count')
        price_from_param = self.request.query_params.get('price_from')
        price_until_param = self.request.query_params.get('price_until')

        if type_param in ['sell', 'rent']:
            queryset = queryset.filter(type=type_param)

        if rooms_count_param:
            queryset = queryset.filter(rooms_count=rooms_count_param)

        if price_from_param:
            queryset = queryset.filter(price__gte=price_from_param)

        if price_until_param:
            queryset = queryset.filter(price__lte=price_until_param)

        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        paginator = self.pagination_class()
        page = paginator.paginate_queryset(queryset, request)
        serializer = self.get_serializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)
