# Generated migration for Version model

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Version',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('version_number', models.CharField(max_length=50, unique=True, verbose_name='Номер версии')),
                ('version_type', models.CharField(choices=[('major', 'Мажорная'), ('minor', 'Минорная'), ('patch', 'Патч'), ('hotfix', 'Хотфикс')], default='minor', max_length=20, verbose_name='Тип версии')),
                ('status', models.CharField(choices=[('draft', 'Черновик'), ('planned', 'Запланирована'), ('in_development', 'В разработке'), ('testing', 'Тестирование'), ('released', 'Выпущена'), ('deprecated', 'Устарела')], default='draft', max_length=20, verbose_name='Статус')),
                ('title', models.CharField(max_length=255, verbose_name='Название')),
                ('description', models.TextField(blank=True, verbose_name='Описание')),
                ('release_notes', models.TextField(blank=True, verbose_name='Примечания к выпуску')),
                ('planned_release_date', models.DateField(blank=True, null=True, verbose_name='Планируемая дата выпуска')),
                ('actual_release_date', models.DateField(blank=True, null=True, verbose_name='Фактическая дата выпуска')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Создана')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Обновлена')),
                ('is_current', models.BooleanField(default=False, verbose_name='Текущая версия')),
                ('changelog', models.JSONField(blank=True, default=dict, verbose_name='История изменений')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='created_versions', to=settings.AUTH_USER_MODEL, verbose_name='Создал')),
                ('released_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='released_versions', to=settings.AUTH_USER_MODEL, verbose_name='Выпустил')),
            ],
            options={
                'verbose_name': 'Версия',
                'verbose_name_plural': 'Версии',
                'ordering': ['-created_at'],
            },
        ),
        migrations.AddIndex(
            model_name='version',
            index=models.Index(fields=['version_number'], name='version_man_version_idx'),
        ),
        migrations.AddIndex(
            model_name='version',
            index=models.Index(fields=['status'], name='version_man_status_idx'),
        ),
        migrations.AddIndex(
            model_name='version',
            index=models.Index(fields=['is_current'], name='version_man_is_curr_idx'),
        ),
    ]

