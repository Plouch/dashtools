<template>
  <div class="app">
    <button 
      v-if="!sidebarVisible" 
      class="sidebar-toggle-btn"
      @click="toggleSidebar"
      aria-label="Show sidebar"
    >
      <span class="toggle-icon">☰</span>
    </button>
    
    <div 
      v-if="sidebarVisible" 
      class="sidebar-overlay"
      @click="toggleSidebar"
      aria-label="Close sidebar"
    ></div>
    
    <aside class="sidebar" :class="{ 'sidebar-hidden': !sidebarVisible }">
      <div class="sidebar-header">
        <div class="header-content">
          <h1 class="app-title">DashTools</h1>
          <p class="app-subtitle">Tools Web Application</p>
        </div>
        <button 
          class="sidebar-close-btn"
          @click="toggleSidebar"
          aria-label="Hide sidebar"
        >
          <span class="close-icon">✕</span>
        </button>
      </div>
      
      <nav class="sidebar-nav">
        <router-link to="/" class="nav-item" active-class="active">
          <span class="nav-icon">🏠</span>
          <span class="nav-text">Home</span>
        </router-link>
        
        <div v-for="category in categories" :key="category" class="nav-section">
          <div class="nav-category">{{ category }}</div>
          <router-link
            v-for="plugin in getPluginsByCategoryWrapper(category)"
            :key="plugin.metadata.id"
            :to="`/plugin/${plugin.metadata.id}`"
            class="nav-item"
            active-class="active"
          >
            <span class="nav-icon">{{ plugin.metadata.icon }}</span>
            <span class="nav-text">{{ plugin.metadata.name }}</span>
          </router-link>
        </div>
      </nav>
      
      <ThemeSelector />
    </aside>
    
    <main class="main-content">
      <router-view />
    </main>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, onMounted } from 'vue'
import { getCategories, getPluginsByCategory } from '@/plugins'
import { useTheme } from '@/composables/useTheme'
import ThemeSelector from '@/components/ThemeSelector.vue'

const categories = computed(() => getCategories())
useTheme() // Initialize theme system

const sidebarVisible = ref(true)

// Load sidebar state from localStorage on mount
onMounted(() => {
  const saved = localStorage.getItem('dashtools-sidebar-visible')
  if (saved !== null) {
    sidebarVisible.value = saved === 'true'
  }
})

function toggleSidebar() {
  sidebarVisible.value = !sidebarVisible.value
  localStorage.setItem('dashtools-sidebar-visible', String(sidebarVisible.value))
}

function getPluginsByCategoryWrapper(category: string) {
  return getPluginsByCategory(category)
}
</script>

<style>
@import '@/styles/themes.css';

* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
  background-color: var(--bg-base);
  color: var(--fg-base);
  transition: background-color 0.3s ease, color 0.3s ease;
}

#app {
  width: 100%;
  height: 100vh;
}
</style>

<style scoped>
.app {
  display: flex;
  height: 100vh;
  overflow: hidden;
}

.sidebar {
  width: 280px;
  background: var(--bg-surface);
  border-right: 1px solid var(--border);
  display: flex;
  flex-direction: column;
  overflow-y: auto;
  transition: transform 0.3s ease, background-color 0.3s ease, border-color 0.3s ease;
  position: relative;
  z-index: 100;
}

@media (max-width: 768px) {
  .sidebar {
    position: fixed;
    left: 0;
    top: 0;
    height: 100vh;
    z-index: 1000;
    box-shadow: 2px 0 8px rgba(0, 0, 0, 0.1);
  }
  
  .sidebar.sidebar-hidden {
    transform: translateX(-100%);
  }
}

@media (min-width: 769px) {
  .sidebar.sidebar-hidden {
    transform: translateX(-100%);
  }
}

.sidebar-header {
  padding: 1.5rem;
  border-bottom: 1px solid var(--border);
  background: var(--bg-overlay);
  transition: background-color 0.3s ease, border-color 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
}

.header-content {
  flex: 1;
  min-width: 0;
}

.app-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--accent);
  margin: 0 0 0.25rem 0;
  transition: color 0.3s ease;
}

.app-subtitle {
  font-size: 0.875rem;
  color: var(--fg-muted);
  margin: 0;
  transition: color 0.3s ease;
}

.sidebar-nav {
  flex: 1;
  padding: 1rem 0;
}

.nav-section {
  margin-bottom: 1.5rem;
}

.nav-category {
  padding: 0.5rem 1.5rem;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  color: var(--fg-muted);
  letter-spacing: 0.5px;
  transition: color 0.3s ease;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1.5rem;
  color: var(--fg-base);
  text-decoration: none;
  transition: background 0.2s ease, color 0.2s ease;
  cursor: pointer;
}

.nav-item:hover {
  background: var(--bg-muted);
}

.nav-item.active {
  background: var(--highlight-low);
  color: var(--accent);
  font-weight: 500;
}

.nav-icon {
  font-size: 1.25rem;
  flex-shrink: 0;
}

.nav-text {
  font-size: 0.9375rem;
}

.main-content {
  flex: 1;
  overflow-y: auto;
  background: var(--bg-base);
  transition: background-color 0.3s ease;
  position: relative;
}

.sidebar-toggle-btn {
  position: fixed;
  top: 1rem;
  left: 1rem;
  z-index: 999;
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 0.75rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: background-color 0.2s ease, border-color 0.2s ease, transform 0.2s ease;
}

.sidebar-toggle-btn:hover {
  background: var(--bg-muted);
  transform: scale(1.05);
}

.sidebar-toggle-btn:active {
  transform: scale(0.95);
}

.toggle-icon {
  font-size: 1.25rem;
  color: var(--fg-base);
  line-height: 1;
}

.sidebar-close-btn {
  background: transparent;
  border: none;
  padding: 0.5rem;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 4px;
  transition: background-color 0.2s ease;
  flex-shrink: 0;
  color: var(--fg-muted);
}

.sidebar-close-btn:hover {
  background: var(--bg-muted);
  color: var(--fg-base);
}

.close-icon {
  font-size: 1.25rem;
  line-height: 1;
  font-weight: 300;
}

.sidebar-overlay {
  display: none;
}

@media (max-width: 768px) {
  .sidebar-overlay {
    display: block;
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.5);
    z-index: 999;
    animation: fadeIn 0.3s ease;
  }
  
  .sidebar-toggle-btn {
    top: 0.75rem;
    left: 0.75rem;
  }
}

@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}
</style>

