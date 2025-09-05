#!/bin/bash
"""Entrypoint script for running migrations and starting the application."""

echo "🚀 Starting application entrypoint..."

# Run database migrations
echo "📊 Running database migrations..."
python migrate.py upgrade

if [ $? -eq 0 ]; then
    echo "✅ Database migrations completed successfully"
else
    echo "❌ Database migrations failed"
    exit 1
fi

# Start the application
echo "🌟 Starting FastAPI application..."
exec "$@"