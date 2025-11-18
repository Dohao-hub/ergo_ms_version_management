<template>
    <div class="version-list">
        <div class="d-flex justify-content-between align-items-center mb-4">
            <h2 class="mb-0">Управление версиями</h2>
            <button class="btn btn-primary" @click="openCreateModal">
                <Plus :size="18" class="me-2" />
                Создать версию
            </button>
        </div>

        <!-- Фильтры -->
        <div class="card mb-4">
            <div class="card-body">
                <div class="row g-3">
                    <div class="col-md-4">
                        <label class="form-label">Поиск</label>
                        <input
                            v-model="filters.search"
                            type="text"
                            class="form-control"
                            placeholder="Поиск по номеру, названию..."
                            @input="handleSearch"
                        />
                    </div>
                    <div class="col-md-3">
                        <label class="form-label">Тип версии</label>
                        <select v-model="filters.version_type" class="form-select" @change="loadVersions">
                            <option value="">Все типы</option>
                            <option value="major">Мажорная</option>
                            <option value="minor">Минорная</option>
                            <option value="patch">Патч</option>
                            <option value="hotfix">Хотфикс</option>
                        </select>
                    </div>
                    <div class="col-md-3">
                        <label class="form-label">Статус</label>
                        <select v-model="filters.status" class="form-select" @change="loadVersions">
                            <option value="">Все статусы</option>
                            <option value="draft">Черновик</option>
                            <option value="planned">Запланирована</option>
                            <option value="in_development">В разработке</option>
                            <option value="testing">Тестирование</option>
                            <option value="released">Выпущена</option>
                            <option value="deprecated">Устарела</option>
                        </select>
                    </div>
                    <div class="col-md-2">
                        <label class="form-label">Текущая</label>
                        <select v-model="filters.is_current" class="form-select" @change="loadVersions">
                            <option value="">Все</option>
                            <option value="true">Да</option>
                            <option value="false">Нет</option>
                        </select>
                    </div>
                </div>
            </div>
        </div>

        <!-- Таблица версий -->
        <div class="card">
            <div class="card-body">
                <div v-if="loading" class="text-center py-5">
                    <div class="spinner-border" role="status">
                        <span class="visually-hidden">Загрузка...</span>
                    </div>
                </div>

                <div v-else-if="versions.length === 0" class="text-center py-5 text-muted">
                    Версии не найдены
                </div>

                <div v-else class="table-responsive">
                    <table class="table table-hover">
                        <thead>
                            <tr>
                                <th>Номер версии</th>
                                <th>Название</th>
                                <th>Тип</th>
                                <th>Статус</th>
                                <th>Дата создания</th>
                                <th>Планируемая дата</th>
                                <th>Текущая</th>
                                <th>Действия</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="version in versions" :key="version.id">
                                <td>
                                    <strong>{{ version.version_number }}</strong>
                                </td>
                                <td>{{ version.title }}</td>
                                <td>
                                    <span class="badge" :class="getTypeBadgeClass(version.version_type)">
                                        {{ getTypeLabel(version.version_type) }}
                                    </span>
                                </td>
                                <td>
                                    <span class="badge" :class="getStatusBadgeClass(version.status)">
                                        {{ getStatusLabel(version.status) }}
                                    </span>
                                </td>
                                <td>{{ formatDate(version.created_at) }}</td>
                                <td>{{ version.planned_release_date ? formatDate(version.planned_release_date) : '-' }}</td>
                                <td>
                                    <span v-if="version.is_current" class="badge bg-success">Текущая</span>
                                    <span v-else>-</span>
                                </td>
                                <td>
                                    <div class="btn-group btn-group-sm">
                                        <button
                                            class="btn btn-outline-primary"
                                            @click="openEditModal(version)"
                                            title="Редактировать"
                                        >
                                            <Edit :size="16" />
                                        </button>
                                        <button
                                            v-if="version.status !== 'released'"
                                            class="btn btn-outline-success"
                                            @click="handleRelease(version)"
                                            title="Выпустить"
                                        >
                                            <Rocket :size="16" />
                                        </button>
                                        <button
                                            v-if="version.status === 'released' && !version.is_current"
                                            class="btn btn-outline-info"
                                            @click="handleSetCurrent(version)"
                                            title="Установить как текущую"
                                        >
                                            <Star :size="16" />
                                        </button>
                                        <button
                                            class="btn btn-outline-danger"
                                            @click="handleDelete(version)"
                                            title="Удалить"
                                        >
                                            <Trash2 :size="16" />
                                        </button>
                                    </div>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>

                <!-- Пагинация -->
                <div v-if="pagination.total_pages > 1" class="d-flex justify-content-between align-items-center mt-4">
                    <div>
                        Показано {{ (pagination.current_page - 1) * pagination.page_size + 1 }} - 
                        {{ Math.min(pagination.current_page * pagination.page_size, pagination.count) }} 
                        из {{ pagination.count }}
                    </div>
                    <nav>
                        <ul class="pagination mb-0">
                            <li class="page-item" :class="{ disabled: !pagination.previous }">
                                <button class="page-link" @click="loadPage(pagination.current_page - 1)" :disabled="!pagination.previous">
                                    Предыдущая
                                </button>
                            </li>
                            <li class="page-item" :class="{ active: page === pagination.current_page }" v-for="page in paginationPages" :key="page">
                                <button class="page-link" @click="loadPage(page)">{{ page }}</button>
                            </li>
                            <li class="page-item" :class="{ disabled: !pagination.next }">
                                <button class="page-link" @click="loadPage(pagination.current_page + 1)" :disabled="!pagination.next">
                                    Следующая
                                </button>
                            </li>
                        </ul>
                    </nav>
                </div>
            </div>
        </div>

        <!-- Модальное окно создания/редактирования -->
        <VersionFormModal
            v-if="showModal"
            :version="editingVersion"
            @close="closeModal"
            @saved="handleSaved"
        />

        <!-- Диалог подтверждения удаления -->
        <ConfirmDialog
            v-if="showDeleteDialog"
            :show="showDeleteDialog"
            title="Подтверждение удаления"
            :message="`Вы уверены, что хотите удалить версию ${versionToDelete?.version_number}?`"
            confirm-text="Удалить"
            cancel-text="Отменить"
            @confirm="confirmDelete"
            @cancel="cancelDelete"
        />
    </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { Plus, Edit, Trash2, Rocket, Star } from 'lucide-vue-next'
import { versionApiService } from '../js/versionApi.js'
import { useToast } from 'vue-toastification'
import ConfirmDialog from '@/components/ConfirmDialog.vue'
import VersionFormModal from './VersionFormModal.vue'

const toast = useToast()

const versions = ref([])
const loading = ref(false)
const showModal = ref(false)
const editingVersion = ref(null)
const showDeleteDialog = ref(false)
const versionToDelete = ref(null)

const filters = ref({
    search: '',
    version_type: '',
    status: '',
    is_current: '',
    ordering: '-created_at'
})

const pagination = ref({
    current_page: 1,
    total_pages: 1,
    page_size: 10,
    count: 0,
    previous: null,
    next: null
})

const paginationPages = computed(() => {
    const pages = []
    const total = pagination.value.total_pages
    const current = pagination.value.current_page
    
    let start = Math.max(1, current - 2)
    let end = Math.min(total, current + 2)
    
    if (end - start < 4) {
        if (start === 1) {
            end = Math.min(5, total)
        } else {
            start = Math.max(1, total - 4)
        }
    }
    
    for (let i = start; i <= end; i++) {
        pages.push(i)
    }
    
    return pages
})

let searchTimeout = null

const handleSearch = () => {
    clearTimeout(searchTimeout)
    searchTimeout = setTimeout(() => {
        pagination.value.current_page = 1
        loadVersions()
    }, 500)
}

const loadVersions = async () => {
    loading.value = true
    try {
        const params = {
            page: pagination.value.current_page,
            page_size: pagination.value.page_size,
            ...filters.value
        }
        
        // Убираем пустые фильтры
        Object.keys(params).forEach(key => {
            if (params[key] === '') {
                delete params[key]
            }
        })
        
        const response = await versionApiService.getVersions(params)
        
        if (response.data.results) {
            versions.value = response.data.results
            pagination.value = {
                current_page: response.data.current_page || 1,
                total_pages: response.data.total_pages || 1,
                page_size: response.data.page_size || 10,
                count: response.data.count || 0,
                previous: response.data.previous,
                next: response.data.next
            }
        } else {
            versions.value = response.data
        }
    } catch (error) {
        toast.error('Ошибка при загрузке версий')
        console.error(error)
    } finally {
        loading.value = false
    }
}

const loadPage = (page) => {
    if (page >= 1 && page <= pagination.value.total_pages) {
        pagination.value.current_page = page
        loadVersions()
    }
}

const openCreateModal = () => {
    editingVersion.value = null
    showModal.value = true
}

const openEditModal = (version) => {
    editingVersion.value = version
    showModal.value = true
}

const closeModal = () => {
    showModal.value = false
    editingVersion.value = null
}

const handleSaved = () => {
    closeModal()
    loadVersions()
    toast.success('Версия успешно сохранена')
}

const handleRelease = async (version) => {
    try {
        await versionApiService.releaseVersion(version.id)
        toast.success('Версия успешно выпущена')
        loadVersions()
    } catch (error) {
        toast.error('Ошибка при выпуске версии')
        console.error(error)
    }
}

const handleSetCurrent = async (version) => {
    try {
        await versionApiService.setCurrentVersion(version.id)
        toast.success('Версия установлена как текущая')
        loadVersions()
    } catch (error) {
        toast.error('Ошибка при установке текущей версии')
        console.error(error)
    }
}

const handleDelete = (version) => {
    versionToDelete.value = version
    showDeleteDialog.value = true
}

const confirmDelete = async () => {
    if (!versionToDelete.value) return
    
    try {
        await versionApiService.deleteVersion(versionToDelete.value.id)
        toast.success('Версия успешно удалена')
        showDeleteDialog.value = false
        versionToDelete.value = null
        loadVersions()
    } catch (error) {
        toast.error('Ошибка при удалении версии')
        console.error(error)
    }
}

const cancelDelete = () => {
    showDeleteDialog.value = false
    versionToDelete.value = null
}

const getTypeLabel = (type) => {
    const labels = {
        major: 'Мажорная',
        minor: 'Минорная',
        patch: 'Патч',
        hotfix: 'Хотфикс'
    }
    return labels[type] || type
}

const getTypeBadgeClass = (type) => {
    const classes = {
        major: 'bg-danger',
        minor: 'bg-primary',
        patch: 'bg-info',
        hotfix: 'bg-warning'
    }
    return classes[type] || 'bg-secondary'
}

const getStatusLabel = (status) => {
    const labels = {
        draft: 'Черновик',
        planned: 'Запланирована',
        in_development: 'В разработке',
        testing: 'Тестирование',
        released: 'Выпущена',
        deprecated: 'Устарела'
    }
    return labels[status] || status
}

const getStatusBadgeClass = (status) => {
    const classes = {
        draft: 'bg-secondary',
        planned: 'bg-info',
        in_development: 'bg-primary',
        testing: 'bg-warning',
        released: 'bg-success',
        deprecated: 'bg-dark'
    }
    return classes[status] || 'bg-secondary'
}

const formatDate = (dateString) => {
    if (!dateString) return '-'
    const date = new Date(dateString)
    return date.toLocaleDateString('ru-RU', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit'
    })
}

onMounted(() => {
    loadVersions()
})
</script>

<style scoped>
.version-list {
    padding: 1rem;
}

.btn-group-sm .btn {
    padding: 0.25rem 0.5rem;
}

.badge {
    font-size: 0.75rem;
    padding: 0.35em 0.65em;
}
</style>

