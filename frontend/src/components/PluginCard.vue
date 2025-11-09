<template>
  <div class="plugin-card" @click="navigateToPlugin">
    <div class="plugin-icon">{{ plugin.metadata.icon }}</div>
    <div class="plugin-info">
      <h3 class="plugin-name">{{ plugin.metadata.name }}</h3>
      <p class="plugin-description">{{ plugin.metadata.description }}</p>
      <span class="plugin-category">{{ plugin.metadata.category }}</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'
import type { Plugin } from '@/types/plugin'

interface Props {
  plugin: Plugin
}

const props = defineProps<Props>()
const router = useRouter()

function navigateToPlugin() {
  router.push(`/plugin/${props.plugin.metadata.id}`)
}
</script>

<style scoped>
.plugin-card {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
  border: 1px solid var(--border);
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.2s ease;
  background: var(--bg-surface);
}

.plugin-card:hover {
  border-color: var(--accent);
  box-shadow: 0 2px 8px var(--highlight-med);
  transform: translateY(-2px);
}

.plugin-icon {
  font-size: 2rem;
  flex-shrink: 0;
}

.plugin-info {
  flex: 1;
  min-width: 0;
}

.plugin-name {
  margin: 0 0 0.5rem 0;
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--fg-base);
  transition: color 0.3s ease;
}

.plugin-description {
  margin: 0 0 0.5rem 0;
  font-size: 0.9rem;
  color: var(--fg-muted);
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  transition: color 0.3s ease;
}

.plugin-category {
  display: inline-block;
  padding: 0.25rem 0.5rem;
  background: var(--bg-muted);
  border-radius: 4px;
  font-size: 0.75rem;
  color: var(--fg-muted);
  transition: background-color 0.3s ease, color 0.3s ease;
}
</style>

