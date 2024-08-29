#!/bin/sh
set -e

echo "â³ Waiting for Metabase to start..."

# Wait for Metabase to be ready
until curl -sf http://metabase:3000/api/health > /dev/null 2>&1; do
    printf '.'
    sleep 3
done

echo ""
echo "âœ“ Metabase is ready!"

# Get setup token
echo "ðŸ”‘ Getting setup token..."
SETUP_TOKEN=""
MAX_RETRIES=30
RETRY_COUNT=0

while [ -z "$SETUP_TOKEN" ] || [ "$SETUP_TOKEN" = "null" ]; do
    if [ $RETRY_COUNT -ge $MAX_RETRIES ]; then
        echo "Failed to get setup token after $MAX_RETRIES attempts"
        exit 1
    fi
    
    sleep 2
    RESPONSE=$(curl -sf http://metabase:3000/api/session/properties 2>/dev/null || echo '{}')
    SETUP_TOKEN=$(echo "$RESPONSE" | grep -o '"setup-token":"[^"]*"' | cut -d'"' -f4)
    RETRY_COUNT=$((RETRY_COUNT + 1))
    printf '.'
done

echo ""
echo "âœ“ Setup token obtained"

# Initial setup
echo "ðŸ‘¤ Creating admin user..."
SESSION_ID=$(curl -sf -X POST http://metabase:3000/api/setup \
    -H "Content-Type: application/json" \
    -d "{
        \"token\": \"$SETUP_TOKEN\",
        \"user\": {
            \"email\": \"admin@newlinex.dev\",
            \"first_name\": \"Admin\",
            \"last_name\": \"User\",
            \"password\": \"NewlineX2024!\"
        },
        \"prefs\": {
            \"allow_tracking\": false,
            \"site_name\": \"NewlineX Sales Analytics\"
        }
    }" | grep -o '"id":"[^"]*"' | cut -d'"' -f4)

echo "âœ“ Admin user created"

# Login to get session
echo "ðŸ” Logging in..."
SESSION=$(curl -sf -X POST http://metabase:3000/api/session \
    -H "Content-Type: application/json" \
    -d '{
        "username": "admin@newlinex.dev",
        "password": "NewlineX2024!"
    }' | grep -o '"id":"[^"]*"' | cut -d'"' -f4)

if [ -z "$SESSION" ]; then
    echo "Login failed"
    exit 1
fi

echo "âœ“ Logged in successfully"

# Add Trino database connection
echo "ðŸ”Œ Adding Trino database connection..."
curl -sf -X POST http://metabase:3000/api/database \
    -H "Content-Type: application/json" \
    -H "X-Metabase-Session: $SESSION" \
    -d '{
        "engine": "starburst",
        "name": "NewlineX Analytics (Trino)",
        "details": {
            "host": "trino",
            "port": 8081,
            "catalog": "delta",
            "schema": "analytics",
            "user": "metabase",
            "ssl": false
        },
        "is_full_sync": true,
        "auto_run_queries": true
