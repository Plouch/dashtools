<template>
  <div class="home">
    <h1 class="home-title">Welcome to DashTools</h1>
    <p class="home-subtitle">Select a plugin from the sidebar to get started</p>
    
    <div v-if="categories.length > 0" class="categories">
      <div v-for="category in categories" :key="category" class="category-section">
        <h2 class="category-title">{{ category }}</h2>
        <div class="plugins-grid">
          <PluginCard
            v-for="plugin in getPluginsByCategory(category)"
            :key="plugin.metadata.id"
            :plugin="plugin"
          />
        </div>
      </div>
    </div>
    
    <div v-else class="empty-state">
      <p>No plugins available</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { getCategories, getPluginsByCategory } from '@/plugins'
import PluginCard from './PluginCard.vue'

const categories = computed(() => getCategories())
</script>

<style scoped>
.home {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.home-title {
  font-size: 2.5rem;
  margin: 0 0 0.5rem 0;
  color: var(--fg-base);
  transition: color 0.3s ease;
}

.home-subtitle {
  font-size: 1.1rem;
  color: var(--fg-muted);
  margin: 0 0 2rem 0;
  transition: color 0.3s ease;
}

.categories {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.category-section {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.category-title {
  font-size: 1.5rem;
  margin: 0;
  color: var(--fg-base);
  font-weight: 600;
  transition: color 0.3s ease;
}

.plugins-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1rem;
}

.empty-state {
  text-align: center;
  padding: 3rem;
  color: var(--fg-muted);
  font-size: 1.1rem;
  transition: color 0.3s ease;
}
</style>

