import uuid
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Version(models.Model):
    """
    Модель для управления версиями системы
    """
    VERSION_TYPE_CHOICES = [
        ('major', 'Мажорная'),
        ('minor', 'Минорная'),
        ('patch', 'Патч'),
        ('hotfix', 'Хотфикс'),
    ]
    
    STATUS_CHOICES = [
        ('draft', 'Черновик'),
        ('planned', 'Запланирована'),
        ('in_development', 'В разработке'),
        ('testing', 'Тестирование'),
        ('released', 'Выпущена'),
        ('deprecated', 'Устарела'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    version_number = models.CharField(max_length=50, unique=True, verbose_name='Номер версии')
    version_type = models.CharField(max_length=20, choices=VERSION_TYPE_CHOICES, default='minor', verbose_name='Тип версии')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', verbose_name='Статус')
    
    title = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')
    release_notes = models.TextField(blank=True, verbose_name='Примечания к выпуску')
    
    # Даты
    planned_release_date = models.DateField(null=True, blank=True, verbose_name='Планируемая дата выпуска')
    actual_release_date = models.DateField(null=True, blank=True, verbose_name='Фактическая дата выпуска')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создана')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлена')
    
    # Связи
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_versions', verbose_name='Создал')
    released_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='released_versions', verbose_name='Выпустил')
    
    # Дополнительная информация
    is_current = models.BooleanField(default=False, verbose_name='Текущая версия')
    changelog = models.JSONField(default=dict, blank=True, verbose_name='История изменений')
    
    class Meta:
        verbose_name = 'Версия'
        verbose_name_plural = 'Версии'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['version_number']),
            models.Index(fields=['status']),
            models.Index(fields=['is_current']),
        ]
    
    def __str__(self):
        return f"{self.version_number} - {self.title}"
    
    def save(self, *args, **kwargs):
        # Если устанавливаем версию как текущую, снимаем флаг с других версий
        if self.is_current:
            Version.objects.filter(is_current=True).exclude(pk=self.pk).update(is_current=False)
        super().save(*args, **kwargs)

