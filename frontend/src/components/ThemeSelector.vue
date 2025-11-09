<template>
  <div class="theme-selector">
    <div class="theme-selector-header">
      <span class="theme-icon">🎨</span>
      <span class="theme-label">Theme</span>
    </div>
    <div class="theme-options">
      <div class="theme-group">
        <div class="theme-group-label">Rosé Pine</div>
        <div class="theme-buttons">
          <button
            @click="setTheme('rose-pine', 'light')"
            :class="['theme-btn', { active: currentTheme === 'rose-pine' && currentVariant === 'light' }]"
            title="Rosé Pine Light"
          >
            ☀️ Light
          </button>
          <button
            @click="setTheme('rose-pine', 'dark')"
            :class="['theme-btn', { active: currentTheme === 'rose-pine' && currentVariant === 'dark' }]"
            title="Rosé Pine Dark"
          >
            🌙 Dark
          </button>
        </div>
      </div>
      <div class="theme-group">
        <div class="theme-group-label">Everforest</div>
        <div class="theme-buttons">
          <button
            @click="setTheme('everforest', 'light')"
            :class="['theme-btn', { active: currentTheme === 'everforest' && currentVariant === 'light' }]"
            title="Everforest Light"
          >
            ☀️ Light
          </button>
          <button
            @click="setTheme('everforest', 'dark')"
            :class="['theme-btn', { active: currentTheme === 'everforest' && currentVariant === 'dark' }]"
            title="Everforest Dark"
          >
            🌙 Dark
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useTheme } from '@/composables/useTheme'
import type { ThemeName, ThemeVariant } from '@/types/theme'

const { currentTheme, currentVariant, setTheme: setThemeState } = useTheme()

function setTheme(theme: ThemeName, variant: ThemeVariant) {
  setThemeState(theme, variant)
}
</script>

<style scoped>
.theme-selector {
  padding: 1rem 1.5rem;
  border-top: 1px solid var(--border);
  background: var(--bg-surface);
}

.theme-selector-header {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 1rem;
}

.theme-icon {
  font-size: 1.25rem;
}

.theme-label {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--fg-base);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.theme-options {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.theme-group {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.theme-group-label {
  font-size: 0.75rem;
  font-weight: 600;
  color: var(--fg-muted);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.theme-buttons {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 0.5rem;
}

.theme-btn {
  padding: 0.5rem 0.75rem;
  border: 1px solid var(--border);
  border-radius: 4px;
  background: var(--bg-overlay);
  color: var(--fg-base);
  font-size: 0.875rem;
  cursor: pointer;
  transition: all 0.2s ease;
  text-align: center;
}

.theme-btn:hover {
  background: var(--bg-muted);
  border-color: var(--border-hover);
}

.theme-btn.active {
  background: var(--accent);
  color: white;
  border-color: var(--accent);
  font-weight: 500;
}

.theme-btn.active:hover {
  background: var(--accent-hover);
}
</style>

