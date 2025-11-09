/**
 * Plugin type definitions
 */

export interface PluginMetadata {
  id: string
  name: string
  description: string
  category: string
  icon: string
  version?: string
}

export interface Plugin {
  metadata: PluginMetadata
  component: any // Vue component
}

