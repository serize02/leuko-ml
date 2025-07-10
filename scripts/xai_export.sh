set -e

DB_FILE="xai.db"
OUTPUT_CSV="outputs/xai_gpt.csv"

echo "[INFO] Exporting data from database to $OUTPUT_CSV..."

sqlite3 -header -csv "$DB_FILE" <<SQL > "$OUTPUT_CSV"
SELECT
  patients.id AS patient_id,
  patients.apache_score,
  patients.leuko_glycemic_index,
  patients.prediction,
  explanations.explanation
FROM patients
LEFT JOIN explanations ON explanations.patient_id = patients.id;
SQL

echo "[INFO] Export complete."