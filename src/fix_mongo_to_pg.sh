#!/bin/bash
set -e

echo "🔎 Step 1: Replacing request.app.mongodb -> session ..."
grep -rl "request.app.mongodb" ./routes | xargs sed -i 's/request.app.mongodb/session/g'

echo "🔎 Step 2: Inserting async session context managers with proper indentation ..."
grep -rn "db_client=session" ./routes | while IFS=: read -r file line _; do
    # Get current line's indentation
    indent=$(sed "${line}q;d" "$file" | sed -E 's/^([ ]*).*$/\1/')
    # Insert async with line above with the same indentation
    sed -i "${line}i\\${indent}async with request.app.db_client() as session:" "$file"
done

echo "✅ Refactor complete. Run black or autopep8 to clean up formatting:"
echo "   black ./routes"

