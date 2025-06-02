#!/bin/bash

SERVER_URL="http://localhost:8080/explain"
INPUT_FILE="outputs/meta-prompts.json"

jq -c '.[]' "$INPUT_FILE" | while read row; do
  PROMPT=$(echo "$row" | jq -r '.prompt')
  APACHE=$(echo "$row" | jq -r '.apache_score')
  LGI=$(echo "$row" | jq -r '.leuko_glycemic_index')
  PREDICTION=$(echo "$row" | jq -r '.prediction')

  RESPONSE=$(curl -s -X POST "$SERVER_URL" \
    -H "Content-Type: application/json" \
    -d "{\"prompt\": \"$PROMPT\"}")

  EXPLANATION=$(echo "$RESPONSE" | jq -r '.explanation // .message // .response // "ERROR"')

  ./xai-db/insert-data "$APACHE" "$LGI" "$PREDICTION" "$EXPLANATION"
done