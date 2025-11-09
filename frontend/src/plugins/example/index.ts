/**
 * Example plugin
 */
import ExamplePlugin from './ExamplePlugin.vue'
import type { Plugin } from '@/types/plugin'

const examplePlugin: Plugin = {
  metadata: {
    id: 'example',
    name: 'Example Plugin',
    description: 'A simple example plugin to demonstrate the plugin system',
    category: 'Utilities',
    icon: '🔧',
    version: '1.0.0'
  },
  component: ExamplePlugin
}

export default examplePlugin

