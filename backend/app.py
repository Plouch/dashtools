"""
Flask backend application for plugin-based web app.
"""
from flask import Flask, jsonify, request
from flask_cors import CORS
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
# Enable CORS for all routes - simple and permissive
CORS(app, origins="*", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"], allow_headers=["Content-Type", "Authorization"])

# Initialize database
from database import init_database
init_database()

# Import plugin registry
from plugins import get_plugins, get_plugin_by_id


@app.route('/api/plugins', methods=['GET'])
def list_plugins():
    """Return list of all available plugins."""
    plugins = get_plugins()
    return jsonify(plugins)


@app.route('/api/plugins/<plugin_id>', methods=['GET'])
def get_plugin(plugin_id):
    """Return metadata for a specific plugin."""
    plugin = get_plugin_by_id(plugin_id)
    if plugin:
        return jsonify(plugin)
    return jsonify({'error': 'Plugin not found'}), 404


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({'status': 'ok'})

@app.after_request
def after_request(response):
    """Add CORS headers to all responses."""
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response


# Database API endpoints
from database import (
    get_tables, get_table_schema, create_table, drop_table,
    add_column, get_table_data, insert_row, update_row, delete_row,
    execute_query
)


@app.route('/api/db/tables', methods=['GET'])
def db_list_tables():
    """Get list of all tables."""
    try:
        tables = get_tables()
        return jsonify({'tables': tables})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/db/tables/<table_name>/schema', methods=['GET'])
def db_get_schema(table_name):
    """Get schema for a table."""
    try:
        schema = get_table_schema(table_name)
        return jsonify({'schema': schema})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/db/tables', methods=['POST', 'OPTIONS'])
def db_create_table():
    """Create a new table."""
    # Handle preflight OPTIONS request
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    
    # Debug logging
    print(f"Received {request.method} request to /api/db/tables")
    print(f"Headers: {dict(request.headers)}")
    print(f"Content-Type: {request.content_type}")
    print(f"Is JSON: {request.is_json}")
    
    try:
        if not request.is_json:
            return jsonify({'error': 'Content-Type must be application/json'}), 400
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Request body is required'}), 400
        
        table_name = data.get('name')
        columns = data.get('columns', [])
        
        if not table_name:
            return jsonify({'error': 'Table name is required'}), 400
        
        success, error_msg = create_table(table_name, columns)
        if success:
            return jsonify({'success': True, 'message': f'Table {table_name} created'})
        else:
            return jsonify({'error': error_msg or 'Failed to create table'}), 400
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"Error in db_create_table: {error_trace}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500


@app.route('/api/db/tables/<table_name>', methods=['DELETE'])
def db_drop_table(table_name):
    """Drop a table."""
    try:
        success = drop_table(table_name)
        if success:
            return jsonify({'success': True, 'message': f'Table {table_name} dropped'})
        else:
            return jsonify({'error': 'Failed to drop table'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/db/tables/<table_name>/columns', methods=['POST'])
def db_add_column(table_name):
    """Add a column to a table."""
    try:
        data = request.get_json()
        column_name = data.get('name')
        column_type = data.get('type', 'TEXT')
        default_value = data.get('default_value')
        
        if not column_name:
            return jsonify({'error': 'Column name is required'}), 400
        
        success = add_column(table_name, column_name, column_type, default_value)
        if success:
            return jsonify({'success': True, 'message': f'Column {column_name} added'})
        else:
            return jsonify({'error': 'Failed to add column'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/db/tables/<table_name>/data', methods=['GET'])
def db_get_data(table_name):
    """Get data from a table."""
    try:
        limit = request.args.get('limit', 100, type=int)
        offset = request.args.get('offset', 0, type=int)
        
        rows, total = get_table_data(table_name, limit, offset)
        return jsonify({
            'data': rows,
            'total': total,
            'limit': limit,
            'offset': offset
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/db/tables/<table_name>/rows', methods=['POST'])
def db_insert_row(table_name):
    """Insert a row into a table."""
    try:
        data = request.get_json()
        success = insert_row(table_name, data)
        if success:
            return jsonify({'success': True, 'message': 'Row inserted'})
        else:
            return jsonify({'error': 'Failed to insert row'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/db/tables/<table_name>/rows/<int:row_id>', methods=['PUT'])
def db_update_row(table_name, row_id):
    """Update a row in a table."""
    try:
        data = request.get_json()
        id_column = data.get('id_column', 'id')
        # Remove id_column from data
        update_data = {k: v for k, v in data.items() if k != 'id_column'}
        
        success = update_row(table_name, row_id, update_data, id_column)
        if success:
            return jsonify({'success': True, 'message': 'Row updated'})
        else:
            return jsonify({'error': 'Failed to update row'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/db/tables/<table_name>/rows/<int:row_id>', methods=['DELETE'])
def db_delete_row(table_name, row_id):
    """Delete a row from a table."""
    try:
        id_column = request.args.get('id_column', 'id')
        success = delete_row(table_name, row_id, id_column)
        if success:
            return jsonify({'success': True, 'message': 'Row deleted'})
        else:
            return jsonify({'error': 'Failed to delete row'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/db/query', methods=['POST'])
def db_execute_query():
    """Execute a SELECT query."""
    try:
        data = request.get_json()
        query = data.get('query', '')
        
        if not query:
            return jsonify({'error': 'Query is required'}), 400
        
        rows, error = execute_query(query)
        if error:
            return jsonify({'error': error}), 400
        
        return jsonify({'data': rows})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    app.run(host=host, port=port, debug=debug)

