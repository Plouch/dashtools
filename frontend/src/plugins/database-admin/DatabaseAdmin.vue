<template>
  <div class="database-admin">
    <div class="plugin-header">
      <h1>{{ metadata.name }}</h1>
      <p>{{ metadata.description }}</p>
    </div>

    <div class="db-content">
      <!-- Sidebar: Table List -->
      <aside class="db-sidebar">
        <div class="sidebar-header">
          <h2>Tables</h2>
          <button @click="showCreateTable = true" class="btn btn-primary btn-sm">
            + New Table
          </button>
        </div>
        <div class="table-list">
          <div
            v-for="table in tables"
            :key="table"
            @click="selectTable(table)"
            :class="['table-item', { active: selectedTable === table }]"
          >
            {{ table }}
          </div>
          <div v-if="tables.length === 0" class="empty-tables">
            No tables found
          </div>
        </div>
      </aside>

      <!-- Main Content: Table Data -->
      <main class="db-main">
        <div v-if="!selectedTable" class="no-selection">
          <p>Select a table from the sidebar to view its data</p>
        </div>

        <div v-else class="table-view">
          <div class="table-header">
            <h2>{{ selectedTable }}</h2>
            <div class="table-actions">
              <button @click="loadTableData" class="btn btn-secondary btn-sm">
                Refresh
              </button>
              <button @click="showAddColumn = true" class="btn btn-secondary btn-sm">
                Add Column
              </button>
              <button @click="showAddRow = true" class="btn btn-primary btn-sm">
                Add Row
              </button>
              <button @click="confirmDeleteTable" class="btn btn-danger btn-sm">
                Delete Table
              </button>
            </div>
          </div>

          <!-- Schema Info -->
          <div class="schema-info">
            <h3>Schema</h3>
            <div class="schema-list">
              <div
                v-for="col in schema"
                :key="col.cid"
                class="schema-item"
              >
                <span class="col-name">{{ col.name }}</span>
                <span class="col-type">{{ col.type }}</span>
                <span v-if="col.pk" class="col-pk">PK</span>
                <span v-if="col.notnull" class="col-null">NOT NULL</span>
              </div>
            </div>
          </div>

          <!-- Data Table -->
          <div class="data-table-container">
            <table class="data-table">
              <thead>
                <tr>
                  <th v-for="col in schema" :key="col.cid">
                    {{ col.name }}
                  </th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="row in tableData" :key="getRowId(row)">
                  <td v-for="col in schema" :key="col.cid">
                    {{ formatCellValue(row[col.name]) }}
                  </td>
                  <td class="actions-cell">
                    <button
                      @click="editRow(row)"
                      class="btn-icon"
                      title="Edit"
                    >
                      ✏️
                    </button>
                    <button
                      @click="confirmDeleteRow(row)"
                      class="btn-icon"
                      title="Delete"
                    >
                      🗑️
                    </button>
                  </td>
                </tr>
                <tr v-if="tableData.length === 0">
                  <td :colspan="schema.length + 1" class="empty-data">
                    No data in this table
                  </td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- Pagination -->
          <div v-if="totalRows > limit" class="pagination">
            <button
              @click="changePage(-1)"
              :disabled="offset === 0"
              class="btn btn-secondary btn-sm"
            >
              Previous
            </button>
            <span class="page-info">
              Showing {{ offset + 1 }} - {{ Math.min(offset + limit, totalRows) }} of {{ totalRows }}
            </span>
            <button
              @click="changePage(1)"
              :disabled="offset + limit >= totalRows"
              class="btn btn-secondary btn-sm"
            >
              Next
            </button>
          </div>
        </div>
      </main>
    </div>

    <!-- Create Table Modal -->
    <div v-if="showCreateTable" class="modal-overlay" @click.self="showCreateTable = false">
      <div class="modal">
        <div class="modal-header">
          <h3>Create New Table</h3>
          <button @click="showCreateTable = false" class="btn-close">×</button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label>Table Name</label>
            <input v-model="newTable.name" type="text" placeholder="table_name" />
          </div>
          <div class="form-group">
            <label>Columns</label>
            <div
              v-for="(col, index) in newTable.columns"
              :key="index"
              class="column-row"
            >
              <input v-model="col.name" type="text" placeholder="column_name" />
              <select v-model="col.type">
                <option value="TEXT">TEXT</option>
                <option value="INTEGER">INTEGER</option>
                <option value="REAL">REAL</option>
                <option value="BLOB">BLOB</option>
              </select>
              <label class="checkbox-label">
                <input v-model="col.primary_key" type="checkbox" />
                PK
              </label>
              <label class="checkbox-label">
                <input v-model="col.not_null" type="checkbox" />
                NOT NULL
              </label>
              <button @click="removeColumn(index)" class="btn-icon">×</button>
            </div>
            <button @click="addColumn" class="btn btn-secondary btn-sm">
              + Add Column
            </button>
          </div>
        </div>
        <div class="modal-footer">
          <button @click="showCreateTable = false" class="btn btn-secondary">
            Cancel
          </button>
          <button @click="createTable" class="btn btn-primary">
            Create Table
          </button>
        </div>
      </div>
    </div>

    <!-- Add Column Modal -->
    <div v-if="showAddColumn" class="modal-overlay" @click.self="showAddColumn = false">
      <div class="modal">
        <div class="modal-header">
          <h3>Add Column to {{ selectedTable }}</h3>
          <button @click="showAddColumn = false" class="btn-close">×</button>
        </div>
        <div class="modal-body">
          <div class="form-group">
            <label>Column Name</label>
            <input v-model="newColumn.name" type="text" placeholder="column_name" />
          </div>
          <div class="form-group">
            <label>Column Type</label>
            <select v-model="newColumn.type">
              <option value="TEXT">TEXT</option>
              <option value="INTEGER">INTEGER</option>
              <option value="REAL">REAL</option>
              <option value="BLOB">BLOB</option>
            </select>
          </div>
          <div class="form-group">
            <label>Default Value (optional)</label>
            <input v-model="newColumn.default_value" type="text" placeholder="default value" />
          </div>
        </div>
        <div class="modal-footer">
          <button @click="showAddColumn = false" class="btn btn-secondary">
            Cancel
          </button>
          <button @click="addColumnToTable" class="btn btn-primary">
            Add Column
          </button>
        </div>
      </div>
    </div>

    <!-- Add/Edit Row Modal -->
    <div v-if="showAddRow || editingRow" class="modal-overlay" @click.self="closeRowModal">
      <div class="modal modal-large">
        <div class="modal-header">
          <h3>{{ editingRow ? 'Edit Row' : 'Add Row' }}</h3>
          <button @click="closeRowModal" class="btn-close">×</button>
        </div>
        <div class="modal-body">
          <div
            v-for="col in schema"
            :key="col.cid"
            class="form-group"
          >
            <label>{{ col.name }} <span v-if="col.pk">(PK)</span></label>
            <input
              v-if="col.type === 'INTEGER' || col.type === 'REAL'"
              v-model.number="rowData[col.name]"
              type="number"
              :disabled="col.pk && editingRow"
            />
            <input
              v-else
              v-model="rowData[col.name]"
              type="text"
              :disabled="col.pk && editingRow"
            />
          </div>
        </div>
        <div class="modal-footer">
          <button @click="closeRowModal" class="btn btn-secondary">
            Cancel
          </button>
          <button @click="saveRow" class="btn btn-primary">
            {{ editingRow ? 'Update' : 'Insert' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import type { PluginMetadata } from '@/types/plugin'

const metadata: PluginMetadata = {
  id: 'database-admin',
  name: 'Database Admin',
  description: 'Administrate your SQLite database: create tables, manage columns, and edit data',
  category: 'Database',
  icon: '🗄️',
  version: '1.0.0'
}

// State
const tables = ref<string[]>([])
const selectedTable = ref<string>('')
const schema = ref<any[]>([])
const tableData = ref<any[]>([])
const totalRows = ref(0)
const limit = ref(50)
const offset = ref(0)

// Modals
const showCreateTable = ref(false)
const showAddColumn = ref(false)
const showAddRow = ref(false)
const editingRow = ref<any>(null)

// Form data
const newTable = ref({
  name: '',
  columns: [{ name: '', type: 'TEXT', primary_key: false, not_null: false }]
})

const newColumn = ref({
  name: '',
  type: 'TEXT',
  default_value: ''
})

const rowData = ref<Record<string, any>>({})

// API functions
async function fetchTables() {
  try {
    const response = await fetch('/api/db/tables')
    const data = await response.json()
    if (data.tables) {
      tables.value = data.tables
    }
  } catch (error) {
    console.error('Error fetching tables:', error)
  }
}

async function fetchSchema(tableName: string) {
  try {
    const response = await fetch(`/api/db/tables/${tableName}/schema`)
    const data = await response.json()
    if (data.schema) {
      schema.value = data.schema
    }
  } catch (error) {
    console.error('Error fetching schema:', error)
  }
}

async function loadTableData() {
  if (!selectedTable.value) return
  
  try {
    const response = await fetch(
      `/api/db/tables/${selectedTable.value}/data?limit=${limit.value}&offset=${offset.value}`
    )
    const data = await response.json()
    if (data.data) {
      tableData.value = data.data
      totalRows.value = data.total
    }
  } catch (error) {
    console.error('Error fetching table data:', error)
  }
}

async function selectTable(tableName: string) {
  selectedTable.value = tableName
  offset.value = 0
  await fetchSchema(tableName)
  await loadTableData()
}

async function createTable() {
  if (!newTable.value.name) {
    alert('Table name is required')
    return
  }

  const validColumns = newTable.value.columns.filter(col => col.name && col.name.trim())
  if (validColumns.length === 0) {
    alert('At least one column with a name is required')
    return
  }

  try {
    const requestBody = {
      name: newTable.value.name,
      columns: validColumns
    }
    
    console.log('Sending request to create table:', requestBody)
    
    const response = await fetch('/api/db/tables', {
      method: 'POST',
      headers: { 
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
      body: JSON.stringify(requestBody)
    })
    
    console.log('Response received:', {
      status: response.status,
      statusText: response.statusText,
      headers: Object.fromEntries(response.headers.entries())
    })
    
    // Read response text once
    const responseText = await response.text()
    const contentType = response.headers.get('content-type')
    
    // Check if response is empty
    if (!responseText || responseText.trim() === '') {
      console.error('Empty response from server:', {
        status: response.status,
        statusText: response.statusText,
        contentType: contentType
      })
      alert(`Server returned empty response (${response.status} ${response.statusText}). Check if backend is running.`)
      return
    }
    
    // Check if response is JSON
    if (!contentType || !contentType.includes('application/json')) {
      console.error('Non-JSON response:', {
        status: response.status,
        statusText: response.statusText,
        contentType: contentType,
        body: responseText.substring(0, 500)
      })
      alert(`Server error: ${response.status} ${response.statusText}\n${responseText.substring(0, 200)}`)
      return
    }
    
    // Parse JSON
    let data
    try {
      data = JSON.parse(responseText)
    } catch (parseError) {
      console.error('JSON parse error:', parseError)
      console.error('Response text:', responseText)
      alert(`Error parsing server response. Check console for details.\nResponse: ${responseText.substring(0, 200)}`)
      return
    }
    
    if (!response.ok) {
      const errorMsg = data.error || `HTTP ${response.status}: Failed to create table`
      console.error('Error creating table:', {
        status: response.status,
        statusText: response.statusText,
        error: data.error,
        data: data
      })
      alert(`Error: ${errorMsg}`)
      return
    }
    
    if (data.success) {
      showCreateTable.value = false
      newTable.value = {
        name: '',
        columns: [{ name: '', type: 'TEXT', primary_key: false, not_null: false }]
      }
      await fetchTables()
      alert('Table created successfully')
    } else {
      const errorMsg = data.error || 'Failed to create table'
      console.error('Failed to create table:', data)
      alert(`Error: ${errorMsg}`)
    }
  } catch (error) {
    console.error('Error creating table:', error)
    alert(`Network error: ${error instanceof Error ? error.message : 'Failed to create table'}`)
  }
}

async function confirmDeleteTable() {
  if (!confirm(`Are you sure you want to delete table "${selectedTable.value}"?`)) {
    return
  }

  try {
    const response = await fetch(`/api/db/tables/${selectedTable.value}`, {
      method: 'DELETE'
    })
    const data = await response.json()
    if (data.success) {
      selectedTable.value = ''
      schema.value = []
      tableData.value = []
      await fetchTables()
      alert('Table deleted successfully')
    } else {
      alert(data.error || 'Failed to delete table')
    }
  } catch (error) {
    console.error('Error deleting table:', error)
    alert('Failed to delete table')
  }
}

async function addColumnToTable() {
  if (!newColumn.value.name) {
    alert('Column name is required')
    return
  }

  try {
    const response = await fetch(`/api/db/tables/${selectedTable.value}/columns`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(newColumn.value)
    })
    const data = await response.json()
    if (data.success) {
      showAddColumn.value = false
      newColumn.value = { name: '', type: 'TEXT', default_value: '' }
      await fetchSchema(selectedTable.value)
      await loadTableData()
      alert('Column added successfully')
    } else {
      alert(data.error || 'Failed to add column')
    }
  } catch (error) {
    console.error('Error adding column:', error)
    alert('Failed to add column')
  }
}

function addColumn() {
  newTable.value.columns.push({
    name: '',
    type: 'TEXT',
    primary_key: false,
    not_null: false
  })
}

function removeColumn(index: number) {
  newTable.value.columns.splice(index, 1)
}

function editRow(row: any) {
  editingRow.value = row
  rowData.value = { ...row }
}

function closeRowModal() {
  showAddRow.value = false
  editingRow.value = null
  rowData.value = {}
}

async function saveRow() {
  if (!selectedTable.value) return

  try {
    let response
    if (editingRow.value) {
      // Update existing row
      const pkColumn = schema.value.find(col => col.pk)?.name || 'id'
      const rowId = editingRow.value[pkColumn]
      response = await fetch(`/api/db/tables/${selectedTable.value}/rows/${rowId}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          ...rowData.value,
          id_column: pkColumn
        })
      })
    } else {
      // Insert new row
      response = await fetch(`/api/db/tables/${selectedTable.value}/rows`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(rowData.value)
      })
    }

    const data = await response.json()
    if (data.success) {
      closeRowModal()
      await loadTableData()
      alert(editingRow.value ? 'Row updated successfully' : 'Row inserted successfully')
    } else {
      alert(data.error || 'Failed to save row')
    }
  } catch (error) {
    console.error('Error saving row:', error)
    alert('Failed to save row')
  }
}

async function confirmDeleteRow(row: any) {
  if (!confirm('Are you sure you want to delete this row?')) {
    return
  }

  try {
    const pkColumn = schema.value.find(col => col.pk)?.name || 'id'
    const rowId = row[pkColumn]
    const response = await fetch(
      `/api/db/tables/${selectedTable.value}/rows/${rowId}?id_column=${pkColumn}`,
      { method: 'DELETE' }
    )
    const data = await response.json()
    if (data.success) {
      await loadTableData()
      alert('Row deleted successfully')
    } else {
      alert(data.error || 'Failed to delete row')
    }
  } catch (error) {
    console.error('Error deleting row:', error)
    alert('Failed to delete row')
  }
}

function changePage(direction: number) {
  offset.value = Math.max(0, offset.value + direction * limit.value)
  loadTableData()
}

function getRowId(row: any): string {
  const pkColumn = schema.value.find(col => col.pk)?.name || 'id'
  return String(row[pkColumn] || Math.random())
}

function formatCellValue(value: any): string {
  if (value === null || value === undefined) return '(null)'
  return String(value)
}

// Initialize
onMounted(async () => {
  await fetchTables()
})
</script>

<style scoped>
.database-admin {
  padding: 2rem;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.plugin-header {
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 2px solid var(--border);
}

.plugin-header h1 {
  font-size: 2rem;
  margin: 0 0 0.5rem 0;
  color: var(--fg-base);
}

.plugin-header p {
  font-size: 1.1rem;
  color: var(--fg-muted);
  margin: 0;
}

.db-content {
  display: flex;
  gap: 1rem;
  flex: 1;
  min-height: 0;
}

.db-sidebar {
  width: 250px;
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 1rem;
  display: flex;
  flex-direction: column;
  overflow-y: auto;
}

.sidebar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}

.sidebar-header h2 {
  font-size: 1.25rem;
  margin: 0;
  color: var(--fg-base);
}

.table-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.table-item {
  padding: 0.75rem;
  background: var(--bg-overlay);
  border: 1px solid var(--border);
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s ease;
  color: var(--fg-base);
}

.table-item:hover {
  background: var(--bg-muted);
  border-color: var(--accent);
}

.table-item.active {
  background: var(--accent);
  color: white;
  border-color: var(--accent);
}

.empty-tables {
  padding: 1rem;
  text-align: center;
  color: var(--fg-muted);
}

.db-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.no-selection {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  color: var(--fg-muted);
  font-size: 1.1rem;
}

.table-view {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  flex: 1;
  min-height: 0;
}

.table-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.table-header h2 {
  font-size: 1.5rem;
  margin: 0;
  color: var(--fg-base);
}

.table-actions {
  display: flex;
  gap: 0.5rem;
}

.schema-info {
  background: var(--bg-overlay);
  border: 1px solid var(--border);
  border-radius: 8px;
  padding: 1rem;
}

.schema-info h3 {
  font-size: 1rem;
  margin: 0 0 0.75rem 0;
  color: var(--fg-base);
}

.schema-list {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.schema-item {
  padding: 0.5rem 0.75rem;
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: 4px;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.875rem;
}

.col-name {
  font-weight: 600;
  color: var(--fg-base);
}

.col-type {
  color: var(--fg-muted);
  font-size: 0.75rem;
}

.col-pk,
.col-null {
  padding: 0.125rem 0.375rem;
  background: var(--accent);
  color: white;
  border-radius: 3px;
  font-size: 0.7rem;
  font-weight: 600;
}

.data-table-container {
  flex: 1;
  overflow: auto;
  border: 1px solid var(--border);
  border-radius: 8px;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
  background: var(--bg-surface);
}

.data-table thead {
  position: sticky;
  top: 0;
  background: var(--bg-overlay);
  z-index: 1;
}

.data-table th {
  padding: 0.75rem;
  text-align: left;
  font-weight: 600;
  color: var(--fg-base);
  border-bottom: 2px solid var(--border);
}

.data-table td {
  padding: 0.75rem;
  border-bottom: 1px solid var(--border);
  color: var(--fg-base);
}

.data-table tbody tr:hover {
  background: var(--bg-muted);
}

.actions-cell {
  display: flex;
  gap: 0.5rem;
}

.btn-icon {
  background: none;
  border: none;
  cursor: pointer;
  font-size: 1.25rem;
  padding: 0.25rem;
  transition: transform 0.2s ease;
}

.btn-icon:hover {
  transform: scale(1.1);
}

.empty-data {
  text-align: center;
  padding: 2rem;
  color: var(--fg-muted);
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  padding: 1rem;
}

.page-info {
  color: var(--fg-muted);
}

/* Modal Styles */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal {
  background: var(--bg-surface);
  border: 1px solid var(--border);
  border-radius: 8px;
  width: 90%;
  max-width: 500px;
  max-height: 90vh;
  display: flex;
  flex-direction: column;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
}

.modal-large {
  max-width: 700px;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid var(--border);
}

.modal-header h3 {
  margin: 0;
  color: var(--fg-base);
}

.btn-close {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: var(--fg-muted);
  padding: 0;
  width: 2rem;
  height: 2rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.btn-close:hover {
  color: var(--fg-base);
}

.modal-body {
  padding: 1.5rem;
  overflow-y: auto;
  flex: 1;
}

.modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 0.5rem;
  padding: 1.5rem;
  border-top: 1px solid var(--border);
}

.form-group {
  margin-bottom: 1rem;
}

.form-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: var(--fg-base);
  font-weight: 500;
}

.form-group input,
.form-group select {
  width: 100%;
  padding: 0.75rem;
  border: 1px solid var(--border);
  border-radius: 4px;
  background: var(--bg-base);
  color: var(--fg-base);
  font-size: 1rem;
}

.form-group input:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.column-row {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
  align-items: center;
}

.column-row input {
  flex: 1;
}

.column-row select {
  width: 120px;
}

.checkbox-label {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  font-size: 0.875rem;
  color: var(--fg-base);
}

.checkbox-label input[type="checkbox"] {
  width: auto;
}

/* Button Styles */
.btn {
  padding: 0.5rem 1rem;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.2s ease;
  font-weight: 500;
}

.btn-primary {
  background: var(--accent);
  color: white;
}

.btn-primary:hover {
  background: var(--accent-hover);
}

.btn-secondary {
  background: var(--bg-muted);
  color: var(--fg-base);
  border: 1px solid var(--border);
}

.btn-secondary:hover {
  background: var(--bg-subtle);
}

.btn-danger {
  background: #d32f2f;
  color: white;
}

.btn-danger:hover {
  background: #c62828;
}

.btn-sm {
  padding: 0.375rem 0.75rem;
  font-size: 0.875rem;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>

