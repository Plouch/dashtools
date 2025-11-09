"""
Plugin registry for backend.
This module maintains a list of available plugins and their metadata.
"""
from typing import List, Dict, Optional

# Plugin registry - add new plugins here
PLUGINS: List[Dict] = [
    {
        'id': 'example',
        'name': 'Example Plugin',
        'description': 'A simple example plugin to demonstrate the plugin system',
        'category': 'Utilities',
        'icon': '🔧',
        'version': '1.0.0'
    },
    {
        'id': 'database-admin',
        'name': 'Database Admin',
        'description': 'Administrate your SQLite database: create tables, manage columns, and edit data',
        'category': 'Database',
        'icon': '🗄️',
        'version': '1.0.0'
    },
    # Add more plugins here as they are created
]


def get_plugins() -> List[Dict]:
    """Return list of all plugins."""
    return PLUGINS.copy()


def get_plugin_by_id(plugin_id: str) -> Optional[Dict]:
    """Return plugin metadata by ID."""
    for plugin in PLUGINS:
        if plugin['id'] == plugin_id:
            return plugin
    return None

