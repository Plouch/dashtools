/**
 * Plugin registry - imports all available plugins
 */
import type { Plugin } from '@/types/plugin'
import examplePlugin from './example'
import databaseAdminPlugin from './database-admin'

const plugins: Plugin[] = [
  examplePlugin,
  databaseAdminPlugin,
  // Add more plugins here as they are created
]

export function getPlugins(): Plugin[] {
  return plugins
}

export function getPluginById(id: string): Plugin | undefined {
  return plugins.find(p => p.metadata.id === id)
}

export function getPluginsByCategory(category: string): Plugin[] {
  return plugins.filter(p => p.metadata.category === category)
}

export function getCategories(): string[] {
  const categories = new Set(plugins.map(p => p.metadata.category))
  return Array.from(categories).sort()
}

export default plugins

