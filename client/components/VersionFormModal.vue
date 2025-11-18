<template>
    <div class="modal fade show d-block" tabindex="-1" @click.self="close" style="background-color: rgba(0,0,0,0.5)">
        <div class="modal-dialog modal-lg modal-dialog-centered">
            <div class="modal-content">
                <div class="modal-header">
                    <h5 class="modal-title">{{ isEditing ? 'Редактировать версию' : 'Создать версию' }}</h5>
                    <button type="button" class="btn-close" @click="close"></button>
                </div>
                <div class="modal-body">
                    <form @submit.prevent="handleSubmit">
                        <div class="row g-3">
                            <div class="col-md-6">
                                <label class="form-label">Номер версии <span class="text-danger">*</span></label>
                                <input
                                    v-model="formData.version_number"
                                    type="text"
                                    class="form-control"
                                    :class="{ 'is-invalid': errors.version_number }"
                                    placeholder="1.0.0"
                                    required
                                />
                                <div v-if="errors.version_number" class="invalid-feedback">
                                    {{ errors.version_number }}
                                </div>
                                <small class="form-text text-muted">Формат: X.Y.Z (например, 1.0.0)</small>
                            </div>

                            <div class="col-md-6">
                                <label class="form-label">Тип версии <span class="text-danger">*</span></label>
                                <select
                                    v-model="formData.version_type"
                                    class="form-select"
                                    :class="{ 'is-invalid': errors.version_type }"
                                    required
                                >
                                    <option value="major">Мажорная</option>
                                    <option value="minor">Минорная</option>
                                    <option value="patch">Патч</option>
                                    <option value="hotfix">Хотфикс</option>
                                </select>
                                <div v-if="errors.version_type" class="invalid-feedback">
                                    {{ errors.version_type }}
                                </div>
                            </div>

                            <div class="col-md-6">
                                <label class="form-label">Статус <span class="text-danger">*</span></label>
                                <select
                                    v-model="formData.status"
                                    class="form-select"
                                    :class="{ 'is-invalid': errors.status }"
                                    required
                                >
                                    <option value="draft">Черновик</option>
                                    <option value="planned">Запланирована</option>
                                    <option value="in_development">В разработке</option>
                                    <option value="testing">Тестирование</option>
                                    <option value="released">Выпущена</option>
                                    <option value="deprecated">Устарела</option>
                                </select>
                                <div v-if="errors.status" class="invalid-feedback">
                                    {{ errors.status }}
                                </div>
                            </div>

                            <div class="col-md-6">
                                <label class="form-label">Планируемая дата выпуска</label>
                                <input
                                    v-model="formData.planned_release_date"
                                    type="date"
                                    class="form-control"
                                    :class="{ 'is-invalid': errors.planned_release_date }"
                                />
                                <div v-if="errors.planned_release_date" class="invalid-feedback">
                                    {{ errors.planned_release_date }}
                                </div>
                            </div>

                            <div class="col-12">
                                <label class="form-label">Название <span class="text-danger">*</span></label>
                                <input
                                    v-model="formData.title"
                                    type="text"
                                    class="form-control"
                                    :class="{ 'is-invalid': errors.title }"
                                    required
                                />
                                <div v-if="errors.title" class="invalid-feedback">
                                    {{ errors.title }}
                                </div>
                            </div>

                            <div class="col-12">
                                <label class="form-label">Описание</label>
                                <textarea
                                    v-model="formData.description"
                                    class="form-control"
                                    :class="{ 'is-invalid': errors.description }"
                                    rows="3"
                                ></textarea>
                                <div v-if="errors.description" class="invalid-feedback">
                                    {{ errors.description }}
                                </div>
                            </div>

                            <div class="col-12">
                                <label class="form-label">Примечания к выпуску</label>
                                <textarea
                                    v-model="formData.release_notes"
                                    class="form-control"
                                    :class="{ 'is-invalid': errors.release_notes }"
                                    rows="4"
                                ></textarea>
                                <div v-if="errors.release_notes" class="invalid-feedback">
                                    {{ errors.release_notes }}
                                </div>
                            </div>

                            <div class="col-12" v-if="formData.status === 'released'">
                                <div class="form-check">
                                    <input
                                        v-model="formData.is_current"
                                        type="checkbox"
                                        class="form-check-input"
                                        id="is_current"
                                    />
                                    <label class="form-check-label" for="is_current">
                                        Установить как текущую версию
                                    </label>
                                </div>
                            </div>
                        </div>
                    </form>
                </div>
                <div class="modal-footer">
                    <button type="button" class="btn btn-secondary" @click="close">Отменить</button>
                    <button type="button" class="btn btn-primary" @click="handleSubmit" :disabled="isSubmitting">
                        <span v-if="isSubmitting" class="spinner-border spinner-border-sm me-2"></span>
                        {{ isEditing ? 'Сохранить' : 'Создать' }}
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { versionApiService } from '../js/versionApi.js'
import { useToast } from 'vue-toastification'

const props = defineProps({
    version: {
        type: Object,
        default: null
    }
})

const emit = defineEmits(['close', 'saved'])

const toast = useToast()

const isEditing = computed(() => !!props.version)

const formData = ref({
    version_number: '',
    version_type: 'minor',
    status: 'draft',
    title: '',
    description: '',
    release_notes: '',
    planned_release_date: '',
    is_current: false
})

const errors = ref({})
const isSubmitting = ref(false)

// Заполнение формы при редактировании
watch(() => props.version, (newVersion) => {
    if (newVersion) {
        formData.value = {
            version_number: newVersion.version_number || '',
            version_type: newVersion.version_type || 'minor',
            status: newVersion.status || 'draft',
            title: newVersion.title || '',
            description: newVersion.description || '',
            release_notes: newVersion.release_notes || '',
            planned_release_date: newVersion.planned_release_date || '',
            is_current: newVersion.is_current || false
        }
    } else {
        // Сброс формы
        formData.value = {
            version_number: '',
            version_type: 'minor',
            status: 'draft',
            title: '',
            description: '',
            release_notes: '',
            planned_release_date: '',
            is_current: false
        }
    }
    errors.value = {}
}, { immediate: true })

const validate = () => {
    errors.value = {}
    
    if (!formData.value.version_number) {
        errors.value.version_number = 'Номер версии обязателен'
    } else {
        const parts = formData.value.version_number.split('.')
        if (parts.length !== 3) {
            errors.value.version_number = 'Номер версии должен быть в формате X.Y.Z'
        } else {
            try {
                parts.forEach(part => {
                    if (isNaN(parseInt(part))) {
                        throw new Error()
                    }
                })
            } catch {
                errors.value.version_number = 'Все части номера версии должны быть числами'
            }
        }
    }
    
    if (!formData.value.title) {
        errors.value.title = 'Название обязательно'
    }
    
    if (formData.value.is_current && formData.value.status !== 'released') {
        errors.value.is_current = 'Текущей может быть только выпущенная версия'
    }
    
    return Object.keys(errors.value).length === 0
}

const handleSubmit = async () => {
    if (!validate()) {
        return
    }
    
    isSubmitting.value = true
    
    try {
        const data = { ...formData.value }
        
        // Убираем пустые поля
        if (!data.planned_release_date) {
            delete data.planned_release_date
        }
        if (!data.description) {
            data.description = ''
        }
        if (!data.release_notes) {
            data.release_notes = ''
        }
        
        if (isEditing.value) {
            await versionApiService.updateVersion(props.version.id, data)
            toast.success('Версия успешно обновлена')
        } else {
            await versionApiService.createVersion(data)
            toast.success('Версия успешно создана')
        }
        
        emit('saved')
    } catch (error) {
        if (error.response?.data) {
            const errorData = error.response.data
            if (typeof errorData === 'object') {
                errors.value = errorData
            } else {
                toast.error(errorData || 'Ошибка при сохранении версии')
            }
        } else {
            toast.error('Ошибка при сохранении версии')
        }
        console.error(error)
    } finally {
        isSubmitting.value = false
    }
}

const close = () => {
    emit('close')
}
</script>

<style scoped>
.modal {
    z-index: 1055;
}

.modal-dialog {
    max-width: 800px;
}

.form-label {
    font-weight: 500;
    margin-bottom: 0.5rem;
}

.text-danger {
    color: #dc3545;
}
</style>

