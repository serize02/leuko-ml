package config

import (
	"log"
	"os"
	"path/filepath"

	"github.com/joho/godotenv"
)

func LoadEnv() {
	envPath, err := filepath.Abs("../.env")
	if err != nil {
		log.Fatalf("Failed to get absolute path for .env: %v", err)
	}

	err = godotenv.Load(envPath)
	if err != nil {
		log.Println("No .env file found (using system env)")
	}
}

func GetOpenAIKey() string {
	key := os.Getenv("OPENAI_API_KEY")
	if key == "" {
		log.Fatal("OPENAI_API_KEY not set")
	}
	return key
}

func GetDBPath() string {
	dbPath, err := filepath.Abs("../xai.db")
	if err != nil {
		log.Fatalf("Failed to get absolute path for DB: %v", err)
	}
	return dbPath
}
