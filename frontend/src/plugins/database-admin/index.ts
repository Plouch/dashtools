/**
 * Database Admin plugin
 */
import DatabaseAdmin from './DatabaseAdmin.vue'
import type { Plugin } from '@/types/plugin'

const databaseAdminPlugin: Plugin = {
  metadata: {
    id: 'database-admin',
    name: 'Database Admin',
    description: 'Administrate your SQLite database: create tables, manage columns, and edit data',
    category: 'Database',
    icon: '🗄️',
    version: '1.0.0'
  },
  component: DatabaseAdmin
}

export default databaseAdminPlugin

