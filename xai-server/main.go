package main

import (
	"database/sql"
	"log"

	"github.com/gin-gonic/gin"
	"github.com/serize02/xai-server/config"
	"github.com/serize02/xai-server/db"
	"github.com/serize02/xai-server/handlers"
	"github.com/serize02/xai-server/openai"

	_ "github.com/mattn/go-sqlite3"
)

func main() {
	config.LoadEnv()
	openai.InitClient()

	dbPath := config.GetDBPath()
	dbConn, err := sql.Open("sqlite3", dbPath)
	if err != nil {
		log.Fatalf("Failed to open database: %v", err)
	}
	defer dbConn.Close()

	db.SetupDatabase(dbConn)

	router := gin.Default()

	router.GET("/ping", func(c *gin.Context) {
		c.JSON(200, gin.H{
			"message": "pong",
		})
	})

	router.POST("/explain", handlers.ExplainHandler(dbConn))

	router.Run(":8080")
}
