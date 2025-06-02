#!/bin/bash

SERVER_URL="http://localhost:8080/explain"
INPUT_FILE="outputs/prompts.json"
OUTPUT_FILE="outputs/explanations.md"

mkdir -p outputs
echo "" > $OUTPUT_FILE

jq -c '.[]' $INPUT_FILE | while read row; do
  PROMPT=$(echo $row | jq -r '.prompt')

  RESPONSE=$(curl -s -X POST "$SERVER_URL" \
    -H "Content-Type: application/json" \
    -d "{\"prompt\": \"$PROMPT\"}")

  EXPLANATION=$(echo $RESPONSE | jq -r '.explanation // .message // .response // "ERROR"')

  { echo 
    echo "$EXPLANATION"
    echo ""
    echo "---"
    echo ""
  } >> $OUTPUT_FILE
done
