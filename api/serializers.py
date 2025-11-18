from rest_framework import serializers
from django.contrib.auth import get_user_model

from .models import Version

User = get_user_model()


class VersionSerializer(serializers.ModelSerializer):
    created_by_username = serializers.CharField(source='created_by.username', read_only=True)
    released_by_username = serializers.CharField(source='released_by.username', read_only=True)
    
    class Meta:
        model = Version
        fields = [
            'id',
            'version_number',
            'version_type',
            'status',
            'title',
            'description',
            'release_notes',
            'planned_release_date',
            'actual_release_date',
            'created_at',
            'updated_at',
            'created_by',
            'created_by_username',
            'released_by',
            'released_by_username',
            'is_current',
            'changelog',
        ]
        read_only_fields = ['created_at', 'updated_at', 'created_by']
    
    def validate_version_number(self, value):
        """Валидация формата номера версии (например, 1.0.0)"""
        parts = value.split('.')
        if len(parts) != 3:
            raise serializers.ValidationError("Номер версии должен быть в формате X.Y.Z (например, 1.0.0)")
        try:
            [int(part) for part in parts]
        except ValueError:
            raise serializers.ValidationError("Все части номера версии должны быть числами")
        return value
    
    def validate(self, attrs):
        """Дополнительная валидация"""
        # Если устанавливаем как текущую версию, проверяем статус
        if attrs.get('is_current', False) and attrs.get('status') != 'released':
            raise serializers.ValidationError({
                'is_current': 'Текущей может быть только выпущенная версия'
            })
        
        # Если указываем фактическую дату выпуска, статус должен быть released
        if attrs.get('actual_release_date') and attrs.get('status') != 'released':
            raise serializers.ValidationError({
                'actual_release_date': 'Фактическая дата выпуска может быть указана только для выпущенной версии'
            })
        
        return attrs
    
    def create(self, validated_data):
        """Создание версии с автоматическим указанием создателя"""
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['created_by'] = request.user
        return super().create(validated_data)

