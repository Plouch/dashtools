<template>
  <div class="example-plugin">
    <div class="plugin-header">
      <h1>{{ metadata.name }}</h1>
      <p>{{ metadata.description }}</p>
    </div>
    
    <div class="plugin-content">
      <div class="demo-section">
        <h2>Counter Demo</h2>
        <div class="counter-display">
          <button @click="decrement" class="btn btn-secondary">-</button>
          <span class="counter-value">{{ count }}</span>
          <button @click="increment" class="btn btn-secondary">+</button>
        </div>
        <button @click="reset" class="btn btn-primary">Reset</button>
      </div>
      
      <div class="demo-section">
        <h2>Text Input Demo</h2>
        <input
          v-model="text"
          type="text"
          placeholder="Type something..."
          class="text-input"
        />
        <p class="output">You typed: <strong>{{ text || '(nothing)' }}</strong></p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import type { PluginMetadata } from '@/types/plugin'

const metadata: PluginMetadata = {
  id: 'example',
  name: 'Example Plugin',
  description: 'A simple example plugin to demonstrate the plugin system',
  category: 'Utilities',
  icon: '🔧',
  version: '1.0.0'
}

const count = ref(0)
const text = ref('')

function increment() {
  count.value++
}

function decrement() {
  count.value--
}

function reset() {
  count.value = 0
  text.value = ''
}
</script>

<style scoped>
.example-plugin {
  padding: 2rem;
  max-width: 800px;
  margin: 0 auto;
}

.plugin-header {
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid var(--border);
  transition: border-color 0.3s ease;
}

.plugin-header h1 {
  font-size: 2rem;
  margin: 0 0 0.5rem 0;
  color: var(--fg-base);
  transition: color 0.3s ease;
}

.plugin-header p {
  font-size: 1.1rem;
  color: var(--fg-muted);
  margin: 0;
  transition: color 0.3s ease;
}

.plugin-content {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.demo-section {
  padding: 1.5rem;
  background: var(--bg-overlay);
  border-radius: 8px;
  border: 1px solid var(--border);
  transition: background-color 0.3s ease, border-color 0.3s ease;
}

.demo-section h2 {
  font-size: 1.25rem;
  margin: 0 0 1rem 0;
  color: var(--fg-base);
  transition: color 0.3s ease;
}

.counter-display {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  margin-bottom: 1rem;
}

.counter-value {
  font-size: 2rem;
  font-weight: 600;
  min-width: 60px;
  text-align: center;
  color: var(--accent);
  transition: color 0.3s ease;
}

.btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-primary {
  background: var(--accent);
  color: white;
  transition: background-color 0.2s ease;
}

.btn-primary:hover {
  background: var(--accent-hover);
}

.btn-secondary {
  background: var(--bg-muted);
  color: var(--fg-base);
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.25rem;
  border: 1px solid var(--border);
  transition: background-color 0.2s ease, border-color 0.2s ease;
}

.btn-secondary:hover {
  background: var(--bg-subtle);
}

.text-input {
  width: 100%;
  padding: 0.75rem;
  font-size: 1rem;
  border: 1px solid var(--border);
  border-radius: 4px;
  margin-bottom: 1rem;
  background: var(--bg-surface);
  color: var(--fg-base);
  transition: border-color 0.2s ease, background-color 0.3s ease, color 0.3s ease;
}

.text-input:focus {
  outline: none;
  border-color: var(--accent);
}

.output {
  margin: 0;
  font-size: 1rem;
  color: var(--fg-muted);
  transition: color 0.3s ease;
}

.output strong {
  color: var(--accent);
  transition: color 0.3s ease;
}
</style>

