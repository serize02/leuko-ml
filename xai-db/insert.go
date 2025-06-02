package main

import (
	"database/sql"
	"fmt"
	"log"
	"os"

	_ "github.com/mattn/go-sqlite3"
)

func main() {
	if len(os.Args) != 5 {
		fmt.Println("Usage: ./insert_patient <apache_score> <leuko_glycemic_index> <prediction> <explanation>")
		os.Exit(1)
	}

	apacheScore := os.Args[1]
	lgi := os.Args[2]
	prediction := os.Args[3]
	explanation := os.Args[4]

	db, err := sql.Open("sqlite3", "data.db")
	if err != nil {
		log.Fatalf("Failed to open database: %v", err)
	}
	defer db.Close()

	res, err := db.Exec(`
		INSERT INTO patients (apache_score, leuko_glycemic_index, prediction)
		VALUES (?, ?, ?)`,
		apacheScore, lgi, prediction,
	)
	if err != nil {
		log.Fatalf("Failed to insert patient: %v", err)
	}

	patientID, err := res.LastInsertId()
	if err != nil {
		log.Fatalf("Failed to retrieve last inserted patient ID: %v", err)
	}

	_, err = db.Exec(`
		INSERT INTO explanations (patient_id, explanation)
		VALUES (?, ?)`,
		patientID, explanation,
	)
	if err != nil {
		log.Fatalf("Failed to insert explanation: %v", err)
	}
}
