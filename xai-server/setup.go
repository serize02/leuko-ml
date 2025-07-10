package main

import (
	"database/sql"
	"log"

	_ "github.com/mattn/go-sqlite3"
	"github.com/serize02/xai-server/config"
)

func main() {
	dbPath := config.GetDBPath()

	db, err := sql.Open("sqlite3", dbPath)
	if err != nil {
		log.Fatalf("Failed to open database: %v", err)
	}
	defer db.Close()

	createPatients := `
	CREATE TABLE IF NOT EXISTS patients (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		apache_score REAL,
		leuko_glycemic_index REAL,
		prediction REAL
	);`

	createExplanations := `
	CREATE TABLE IF NOT EXISTS explanations (
		id INTEGER PRIMARY KEY AUTOINCREMENT,
		patient_id INTEGER,
		explanation TEXT,
		FOREIGN KEY(patient_id) REFERENCES patients(id)
	);`

	_, err = db.Exec(createPatients)
	if err != nil {
		log.Fatalf("Failed to create patients table: %v", err)
	}

	_, err = db.Exec(createExplanations)
	if err != nil {
		log.Fatalf("Failed to create explanations table: %v", err)
	}

	log.Println("Database and tables created (if not exist).")
}
