package main

import (
	"github.com/gin-gonic/gin"
    "github.com/serize02/xai-server/config"
    "github.com/serize02/xai-server/handlers"
    "github.com/serize02/xai-server/openai"
)

func main() {
	config.LoadEnv()
	openai.InitClient()

	router := gin.Default()

	router.POST("/explain", handlers.ExplainHandler)

	router.Run(":8080")
}
