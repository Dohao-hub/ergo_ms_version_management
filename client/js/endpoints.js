export const versionManagementEndpoints = {
    versions: {
        list: 'version_management/versions/',
        detail: id => `version_management/versions/${id}/`,
        create: 'version_management/versions/',
        update: id => `version_management/versions/${id}/`,
        delete: id => `version_management/versions/${id}/`,
        setCurrent: id => `version_management/versions/${id}/set_current/`,
        release: id => `version_management/versions/${id}/release/`,
        current: 'version_management/versions/current/',
        latest: 'version_management/versions/latest/',
    }
};

