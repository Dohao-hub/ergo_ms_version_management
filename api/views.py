from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from django.utils import timezone

from core.api.src.core.utils.mixins import SwaggerSafeMixin
from .models import Version
from .serializers import VersionSerializer


class VersionViewSet(SwaggerSafeMixin, viewsets.ModelViewSet):
    """
    ViewSet для управления версиями
    """
    serializer_class = VersionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['version_type', 'status', 'is_current']
    search_fields = ['version_number', 'title', 'description']
    ordering_fields = ['created_at', 'updated_at', 'version_number', 'planned_release_date']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Получение queryset с учетом Swagger"""
        if self.is_swagger_fake_view():
            return Version.objects.none()
        return Version.objects.all()
    
    @action(detail=True, methods=['post'])
    def set_current(self, request, pk=None):
        """Установить версию как текущую"""
        version = self.get_object()
        
        if version.status != 'released':
            return Response(
                {'error': 'Текущей может быть только выпущенная версия'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        version.is_current = True
        version.save()
        
        serializer = self.get_serializer(version)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def release(self, request, pk=None):
        """Выпустить версию"""
        version = self.get_object()
        
        if version.status == 'released':
            return Response(
                {'error': 'Версия уже выпущена'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        version.status = 'released'
        version.actual_release_date = timezone.now().date()
        version.released_by = request.user
        version.save()
        
        serializer = self.get_serializer(version)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def current(self, request):
        """Получить текущую версию"""
        current_version = Version.objects.filter(is_current=True).first()
        
        if not current_version:
            return Response(
                {'error': 'Текущая версия не установлена'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = self.get_serializer(current_version)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def latest(self, request):
        """Получить последнюю выпущенную версию"""
        latest_version = Version.objects.filter(status='released').order_by('-created_at').first()
        
        if not latest_version:
            return Response(
                {'error': 'Нет выпущенных версий'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        serializer = self.get_serializer(latest_version)
        return Response(serializer.data)

