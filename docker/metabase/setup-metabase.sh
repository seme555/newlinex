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

