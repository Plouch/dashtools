/**
 * Plugin registry - imports all available plugins
 */
import type { Plugin } from '@/types/plugin'
import examplePlugin from './example'
import databaseAdminPlugin from './database-admin'

// Import all plugins here
const plugins: Plugin[] = [
  examplePlugin,
  databaseAdminPlugin,
  // Add more plugins here as they are created
]

/**
 * Get all registered plugins
 */
export function getPlugins(): Plugin[] {
  return plugins
}

/**
 * Get a plugin by ID
 */
export function getPluginById(id: string): Plugin | undefined {
  return plugins.find(p => p.metadata.id === id)
}

/**
 * Get plugins by category
 */
export function getPluginsByCategory(category: string): Plugin[] {
  return plugins.filter(p => p.metadata.category === category)
}

/**
 * Get all unique categories
 */
export function getCategories(): string[] {
  const categories = new Set(plugins.map(p => p.metadata.category))
  return Array.from(categories).sort()
}

export default plugins

