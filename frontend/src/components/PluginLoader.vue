<template>
  <div class="plugin-loader">
    <component
      v-if="pluginComponent"
      :is="pluginComponent"
    />
    <div v-else-if="loading" class="loading">
      Loading plugin...
    </div>
    <div v-else class="error">
      Plugin not found
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, watch, ref } from 'vue'
import { useRoute } from 'vue-router'
import { getPluginById } from '@/plugins'

const route = useRoute()
const loading = ref(true)
const pluginComponent = ref<any>(null)

const pluginId = computed(() => route.params.id as string)

function loadPlugin() {
  loading.value = true
  const plugin = getPluginById(pluginId.value)
  if (plugin) {
    pluginComponent.value = plugin.component
  } else {
    pluginComponent.value = null
  }
  loading.value = false
}

// Watch for route parameter changes
watch(pluginId, () => {
  loadPlugin()
}, { immediate: true })
</script>

<style scoped>
.plugin-loader {
  width: 100%;
  height: 100%;
}

.loading,
.error {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  font-size: 1.2rem;
  color: var(--fg-muted);
  transition: color 0.3s ease;
}

.error {
  color: var(--accent);
}
</style>

