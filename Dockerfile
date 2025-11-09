# Multi-stage build for combined frontend and backend

# Stage 1: Build Frontend
FROM node:20-alpine AS frontend-builder

WORKDIR /app

# Copy frontend package files
COPY frontend/package*.json ./

# Install dependencies
RUN npm ci || npm install

# Copy frontend source code
COPY frontend/ .

# Build the application
RUN npm run build

# Stage 2: Final combined image
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies including nginx and supervisor
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    nginx \
    supervisor \
    && rm -rf /var/lib/apt/lists/*

# Copy backend requirements and install Python dependencies
COPY backend/requirements.txt ./backend/
RUN pip install --no-cache-dir -r backend/requirements.txt

# Copy backend application code
COPY backend/ ./backend/

# Copy built frontend from builder stage
COPY --from=frontend-builder /app/dist /usr/share/nginx/html

# Create nginx configuration
RUN mkdir -p /etc/nginx/sites-available /etc/nginx/sites-enabled && \
    rm -f /etc/nginx/sites-enabled/default

# Create nginx config that proxies API to localhost
RUN echo 'server {\n\
    listen 80;\n\
    server_name localhost;\n\
    root /usr/share/nginx/html;\n\
    index index.html;\n\
\n\
    gzip on;\n\
    gzip_vary on;\n\
    gzip_min_length 1024;\n\
    gzip_types text/plain text/css text/xml text/javascript application/x-javascript application/xml+rss application/json;\n\
\n\
    location / {\n\
        try_files $uri $uri/ /index.html;\n\
    }\n\
\n\
    location /api {\n\
        proxy_pass http://127.0.0.1:5000;\n\
        proxy_http_version 1.1;\n\
        proxy_set_header Upgrade $http_upgrade;\n\
        proxy_set_header Connection "upgrade";\n\
        proxy_set_header Host $host;\n\
        proxy_set_header X-Real-IP $remote_addr;\n\
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;\n\
        proxy_set_header X-Forwarded-Proto $scheme;\n\
        proxy_cache_bypass $http_upgrade;\n\
    }\n\
\n\
    location ~* \.(jpg|jpeg|png|gif|ico|css|js|svg|woff|woff2|ttf|eot)$ {\n\
        expires 1y;\n\
        add_header Cache-Control "public, immutable";\n\
    }\n\
}' > /etc/nginx/sites-available/default && \
    ln -s /etc/nginx/sites-available/default /etc/nginx/sites-enabled/default

# Create supervisor configuration
RUN mkdir -p /var/log/supervisor && \
    echo '[supervisord]\n\
nodaemon=true\n\
user=root\n\
\n\
[program:nginx]\n\
command=/usr/sbin/nginx -g "daemon off;"\n\
autostart=true\n\
autorestart=true\n\
stderr_logfile=/var/log/supervisor/nginx.err.log\n\
stdout_logfile=/var/log/supervisor/nginx.out.log\n\
\n\
[program:backend]\n\
command=python /app/backend/app.py\n\
directory=/app/backend\n\
autostart=true\n\
autorestart=true\n\
stderr_logfile=/var/log/supervisor/backend.err.log\n\
stdout_logfile=/var/log/supervisor/backend.out.log\n\
environment=PORT="5000",FLASK_HOST="0.0.0.0"' > /etc/supervisor/conf.d/supervisord.conf

# Create data directory for SQLite
RUN mkdir -p /app/data

# Expose port 80 (nginx will serve frontend and proxy API)
EXPOSE 80

# Set working directory to backend
WORKDIR /app/backend

# Run supervisor to manage both services
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]