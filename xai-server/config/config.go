package config

import (
	"log"
	"os"
	"github.com/joho/godotenv"
)

func LoadEnv() {
	err := godotenv.Load()
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
