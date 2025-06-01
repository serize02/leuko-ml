package handlers

import (
	"context"
	"net/http"
	"github.com/serize02/xai-server/openai"

	"github.com/gin-gonic/gin"
	openaiLib "github.com/sashabaranov/go-openai"
)

type ExplainRequest struct {
	Prompt string `json:"prompt"`
}

func ExplainHandler(c *gin.Context) {
	var req ExplainRequest
	if err := c.ShouldBindJSON(&req); err != nil {
		c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid request"})
		return
	}

	resp, err := openai.Client.CreateChatCompletion(
		context.Background(),
		openaiLib.ChatCompletionRequest{
			Model: openaiLib.GPT3Dot5Turbo,
			Messages: []openaiLib.ChatCompletionMessage{
				{Role: openaiLib.ChatMessageRoleUser, Content: req.Prompt},
			},
		},
	)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"error": "OpenAI request failed"})
		return
	}

	c.JSON(http.StatusOK, gin.H{"response": resp.Choices[0].Message.Content})
}
