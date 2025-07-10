#!/bin/bash
set -e

SERVER_LOG="xai-server/server.log"
INPUT_FILE="outputs/meta_prompts.json"
SERVER_URL="http://localhost:8080/explain"

jq -c '.[]' "$INPUT_FILE" | while read -r row; do
  PROMPT=$(echo "$row" | jq -r '.prompt')
  APACHE=$(echo "$row" | jq -r '.apache_score')
  LGI=$(echo "$row" | jq -r '.leuko_glycemic_index')
  PREDICTION=$(echo "$row" | jq -r '.prediction')

  ESCAPED_PROMPT=$(printf '%s' "$PROMPT" | jq -Rs .)

  PAYLOAD=$(jq -n \
    --argjson apache "$APACHE" \
    --argjson lgi "$LGI" \
    --argjson prediction "$PREDICTION" \
    --arg prompt "$PROMPT" \
    '{prompt: $prompt, apache_score: $apache, leuko_glycemic_index: $lgi, prediction: $prediction}')

  RESPONSE=$(curl -s -X POST "$SERVER_URL" \
    -H "Content-Type: application/json" \
    -d "$PAYLOAD")

  EXPLANATION=$(echo "$RESPONSE" | jq -r '.explanation // .message // .response // "ERROR"')
done
