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
