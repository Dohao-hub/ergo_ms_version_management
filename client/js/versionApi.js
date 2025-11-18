import { apiClient } from '@/js/api/manager'
import { versionManagementEndpoints } from './endpoints.js'

/**
 * Сервис для работы с Version Management API
 */
class VersionApiService {
    constructor() {
        this.endpoints = versionManagementEndpoints.versions
    }

    /**
     * Получить список версий
     * @param {Object} params - Параметры запроса (фильтры, пагинация)
     */
    async getVersions(params = {}) {
        return await apiClient.get(this.endpoints.list, params)
    }

    /**
     * Получить версию по ID
     * @param {string} id - ID версии
     */
    async getVersion(id) {
        return await apiClient.get(this.endpoints.detail(id))
    }

    /**
     * Создать версию
     * @param {Object} data - Данные версии
     */
    async createVersion(data) {
        return await apiClient.post(this.endpoints.create, data)
    }

    /**
     * Обновить версию
     * @param {string} id - ID версии
     * @param {Object} data - Данные версии
     */
    async updateVersion(id, data) {
        return await apiClient.patch(this.endpoints.update(id), data)
    }

    /**
     * Удалить версию
     * @param {string} id - ID версии
     */
    async deleteVersion(id) {
        return await apiClient.delete(this.endpoints.delete(id))
    }

    /**
     * Установить версию как текущую
     * @param {string} id - ID версии
     */
    async setCurrentVersion(id) {
        return await apiClient.post(this.endpoints.setCurrent(id))
    }

    /**
     * Выпустить версию
     * @param {string} id - ID версии
     */
    async releaseVersion(id) {
        return await apiClient.post(this.endpoints.release(id))
    }

    /**
     * Получить текущую версию
     */
    async getCurrentVersion() {
        return await apiClient.get(this.endpoints.current)
    }

    /**
     * Получить последнюю выпущенную версию
     */
    async getLatestVersion() {
        return await apiClient.get(this.endpoints.latest)
    }
}

export const versionApiService = new VersionApiService()

