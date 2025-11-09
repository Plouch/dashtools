# DashTools - Plugin-Based Web Application

A lightweight web application with Flask backend and Vue 3 frontend that allows you to develop and host multiple small applications (plugins) in one central place.  
This is currently a learning project.

## Features

- 🚀 **Lightweight**: Simple architecture, easy to understand and modify
- 🔌 **Plugin System**: Easy-to-add plugins as separate modules
- 🎨 **Modern UI**: Clean, responsive interface with sidebar navigation
- 📦 **TypeScript**: Full type safety for plugins
- 🔄 **Hot Reload**: Fast development with Vite

## Project Structure

```
dashtools/
├── backend/                    # Flask backend
│   ├── app.py                 # Main Flask application
│   ├── database.py            # Database configuration and utilities
│   ├── bootstrap.db           # SQLite database file
│   ├── Dockerfile             # Backend Docker image
│   ├── plugins/               # Backend plugin registry
│   │   └── __init__.py
│   └── requirements.txt        # Python dependencies
├── frontend/                  # Vue 3 frontend
│   ├── src/
│   │   ├── App.vue           # Root Vue component
│   │   ├── main.ts           # Application entry point
│   │   ├── env.d.ts          # TypeScript environment definitions
│   │   ├── components/       # Shared Vue components
│   │   │   ├── Home.vue
│   │   │   ├── PluginCard.vue
│   │   │   ├── PluginLoader.vue
│   │   │   └── ThemeSelector.vue
│   │   ├── composables/      # Vue composables
│   │   │   └── useTheme.ts
│   │   ├── plugins/          # Plugin components
│   │   │   ├── database-admin/
│   │   │   ├── example/
│   │   │   └── index.ts      # Plugin registry
│   │   ├── router/           # Vue Router configuration
│   │   │   └── index.ts
│   │   ├── styles/           # Global styles
│   │   │   └── themes.css
│   │   └── types/            # TypeScript type definitions
│   │       ├── plugin.ts
│   │       └── theme.ts
│   ├── index.html            # HTML template
│   ├── nginx.conf            # Nginx configuration for production
│   ├── Dockerfile            # Frontend Docker image
│   ├── package.json          # Node.js dependencies
│   ├── package-lock.json     # Dependency lock file
│   ├── vite.config.ts        # Vite configuration
│   ├── tsconfig.json         # TypeScript configuration
│   └── tsconfig.node.json    # TypeScript config for Node.js
├── docker-compose.yml        # Docker Compose configuration
├── Makefile                  # Make commands for common tasks
└── README.md                 # This file
```

## Setup

### Prerequisites

- Python 3.8+
- Node.js 18+
- npm or pnpm
- [uv](https://github.com/astral-sh/uv) (optional, faster alternative to pip)

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a `.env` file (optional, for configuration):
```bash
cp .env.example .env
```

Edit `.env` to configure:
- `PORT`: Backend server port (default: 5000)
- `FLASK_DEBUG`: Enable debug mode (default: True)
- `DATABASE_PATH`: SQLite database file path (default: dashtools.db)

3. Install dependencies:

**Using uv (recommended - faster):**
```bash
# Install uv if you haven't already:
# curl -LsSf https://astral.sh/uv/install.sh | sh
# or: pip install uv
# or: brew install uv

# Create virtual environment and install dependencies:
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -r requirements.txt
```

**Using pip (alternative):**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

4. Run the Flask server:
```bash
python app.py
```

The backend will run on `http://localhost:5000` (or the port specified in `.env`)

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Create a `.env` file (optional, for configuration):
```bash
cp .env.example .env
```

Edit `.env` to configure:
- `VITE_PORT`: Frontend development server port (default: 3000)
- `VITE_API_URL`: Backend API URL for proxy (default: http://localhost:5000)
- `VITE_DEFAULT_THEME`: Default theme name (rose-pine or everforest, default: rose-pine)
- `VITE_DEFAULT_THEME_VARIANT`: Default theme variant (light or dark, default: dark)

3. Install dependencies:
```bash
npm install
# or
pnpm install
```

4. Start the development server:
```bash
npm run dev
# or
pnpm dev
```

The frontend will run on `http://localhost:3000` (or the port specified in `.env`)

## Configuration

The application can be configured using `.env` files in both the backend and frontend directories.

### Backend Configuration (`backend/.env`)

- `PORT`: Port for the Flask backend server (default: 5000)
- `FLASK_DEBUG`: Enable Flask debug mode - True/False (default: True)
- `FLASK_HOST`: Host to bind the Flask server to (default: 0.0.0.0)
- `DATABASE_PATH`: Path to the SQLite database file (default: dashtools.db)

### Frontend Configuration (`frontend/.env`)

- `VITE_PORT`: Port for the Vite development server (default: 3000)
- `VITE_API_URL`: Backend API URL used for proxy configuration (default: http://localhost:5000)
- `VITE_DEFAULT_THEME`: Default theme name - `rose-pine` or `everforest` (default: rose-pine)
- `VITE_DEFAULT_THEME_VARIANT`: Default theme variant - `light` or `dark` (default: dark)

**Note:** After changing `.env` files, you may need to restart the servers for changes to take effect.

## Development

### Running Both Servers

You'll need to run both the backend and frontend servers simultaneously:

**Terminal 1 (Backend):**
```bash
cd backend
python app.py
```

**Terminal 2 (Frontend):**
```bash
cd frontend
npm run dev
```

The Vite dev server is configured to proxy API requests to the Flask backend. Make sure the `VITE_API_URL` in your frontend `.env` matches your backend `PORT` configuration.

## Creating a New Plugin

### Step 1: Create Plugin Directory

Create a new directory in `frontend/src/plugins/` with your plugin name:

```bash
mkdir frontend/src/plugins/my-plugin
```

### Step 2: Create Plugin Component

Create `MyPlugin.vue` in your plugin directory:

```vue
<template>
  <div class="my-plugin">
    <h1>{{ metadata.name }}</h1>
    <p>{{ metadata.description }}</p>
    <!-- Your plugin content here -->
  </div>
</template>

<script setup lang="ts">
import type { PluginMetadata } from '@/types/plugin'

const metadata: PluginMetadata = {
  id: 'my-plugin',
  name: 'My Plugin',
  description: 'Description of my plugin',
  category: 'Utilities',
  icon: '🔧',
  version: '1.0.0'
}

// Your plugin logic here
</script>

<style scoped>
.my-plugin {
  padding: 2rem;
}
</style>
```

### Step 3: Create Plugin Index

Create `index.ts` in your plugin directory:

```typescript
import MyPlugin from './MyPlugin.vue'
import type { Plugin } from '@/types/plugin'

const myPlugin: Plugin = {
  metadata: {
    id: 'my-plugin',
    name: 'My Plugin',
    description: 'Description of my plugin',
    category: 'Utilities',
    icon: '🔧',
    version: '1.0.0'
  },
  component: MyPlugin
}

export default myPlugin
```

### Step 4: Register Plugin

Add your plugin to `frontend/src/plugins/index.ts`:

```typescript
import myPlugin from './my-plugin'

const plugins: Plugin[] = [
  examplePlugin,
  myPlugin,  // Add your plugin here
  // ...
]
```

### Step 5: Register in Backend (Optional)

If you want the backend to know about your plugin, add it to `backend/plugins/__init__.py`:

```python
PLUGINS: List[Dict] = [
    {
        'id': 'example',
        'name': 'Example Plugin',
        # ...
    },
    {
        'id': 'my-plugin',
        'name': 'My Plugin',
        'description': 'Description of my plugin',
        'category': 'Utilities',
        'icon': '🔧',
        'version': '1.0.0'
    },
]
```

## Plugin Interface

All plugins must implement the `Plugin` interface:

```typescript
interface Plugin {
  metadata: PluginMetadata
  component: any // Vue component
}

interface PluginMetadata {
  id: string           // Unique plugin identifier
  name: string         // Display name
  description: string  // Plugin description
  category: string     // Category for grouping
  icon: string         // Emoji or icon
  version?: string     // Optional version
}
```

## API Endpoints

### `GET /api/plugins`
Returns a list of all available plugins.

### `GET /api/plugins/<id>`
Returns metadata for a specific plugin.

### `GET /api/health`
Health check endpoint.

## Building for Production

### Frontend

```bash
cd frontend
npm run build
```

The built files will be in `frontend/dist/`

### Backend

The Flask app can be run with any WSGI server (gunicorn, uwsgi, etc.):

```bash
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## Example Plugin

An example plugin is included in `frontend/src/plugins/example/` that demonstrates:
- Basic plugin structure
- State management with Vue Composition API
- Simple UI components

## Docker Deployment

### Quick Start with Makefile (Recommended)

The easiest way to build and deploy is using the Makefile:

1. **Copy environment file:**
```bash
cp .env.docker.example .env
```

2. **Edit `.env` file** to configure:
   - `DATABASE_TYPE`: Set to `sqlite` (default) or `postgresql`
   - PostgreSQL settings if using PostgreSQL

3. **Quick start with SQLite:**
```bash
make quickstart
```

4. **Quick start with PostgreSQL:**
```bash
make quickstart-db
```

5. **View all available commands:**
```bash
make help
```

The application will be available at:
- Frontend: `http://localhost:80` (or port specified in `.env`)
- Backend API: `http://localhost:5000` (or port specified in `.env`)

### Quick Start with Docker Compose (Alternative)

1. **Copy environment file:**
```bash
cp .env.docker.example .env
```

2. **Edit `.env` file** to configure:
   - `DATABASE_TYPE`: Set to `sqlite` (default) or `postgresql`
   - PostgreSQL settings if using PostgreSQL

3. **Start with SQLite (default):**
```bash
docker-compose up -d
```

4. **Start with PostgreSQL:**
```bash
docker-compose --profile with-db up -d
```

### Docker Compose Services

- **frontend**: Vue.js application served by nginx
- **backend**: Flask API server
- **postgres**: PostgreSQL database (optional, only with `--profile with-db`)

### Using External PostgreSQL

To use an external PostgreSQL database instead of the Docker service:

1. Set `DATABASE_TYPE=postgresql` in your `.env` file
2. Configure PostgreSQL connection:
   ```
   POSTGRES_HOST=your-external-host
   POSTGRES_PORT=5432
   POSTGRES_USER=your-user
   POSTGRES_PASSWORD=your-password
   POSTGRES_DB=your-database
   ```
3. Start without the postgres service:
   ```bash
   docker-compose up -d frontend backend
   ```

### Common Makefile Commands

```bash
make help              # Show all available commands
make build             # Build Docker images
make up                # Start services (SQLite)
make up-db             # Start services with PostgreSQL
make down              # Stop services
make logs              # View logs from all services
make logs-backend      # View backend logs
make logs-frontend     # View frontend logs
make restart           # Restart all services
make clean             # Remove containers and volumes
make status            # Check service status
make dev-backend       # Run backend locally (development)
make dev-frontend      # Run frontend locally (development)
make install           # Install all dependencies locally
```

### Building Images

Build images manually:
```bash
# Using Makefile
make build

# Or using Docker Compose
docker-compose build

# Or manually
docker build -t dashtools-backend ./backend
docker build -t dashtools-frontend ./frontend
```

### Database Migration

When switching from SQLite to PostgreSQL (or vice versa), note that:
- Data is not automatically migrated
- You'll need to recreate tables and data
- The database admin plugin can help with this

## License

This project is open source and available under the GNU GPLv3 License.

## Contributing

Feel free to submit issues and enhancement requests!

