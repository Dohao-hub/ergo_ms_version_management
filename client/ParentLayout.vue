<template>
    <div class="version-management-layout">
        <VersionList />
    </div>
</template>

<script setup>
import VersionList from './components/VersionList.vue'
</script>

<style scoped>
.version-management-layout {
    min-height: 100vh;
    background-color: #f8f9fa;
}
</style>