SERVER_URL="http://localhost:8080/explain"
INPUT_FILE="outputs/prompts.json"
OUTPUT_FILE="outputs/explanations.csv"

mkdir -p outputs
echo "id,explanation" > $OUTPUT_FILE

jq -c '.[]' $INPUT_FILE | while read row; do
  
  ID=$(echo $row | jq '.id')
  PROMPT=$(echo $row | jq -r '.prompt')

  RESPONSE=$(curl -s -X POST "$SERVER_URL" \
    -H "Content-Type: application/json" \
    -d "{\"prompt\": \"$PROMPT\"}")

  EXPLANATION=$(echo $RESPONSE | jq -r '.explanation // .message // .response // "ERROR"')

  echo "$ID,\"$EXPLANATION\"" >> $OUTPUT_FILE
done