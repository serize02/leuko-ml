package handlers

import (
	"context"
	"database/sql"
	"fmt"
	"net/http"

	"github.com/gin-gonic/gin"
	"github.com/serize02/xai-server/openai"
	openaiLib "github.com/sashabaranov/go-openai"
)

type ExplainRequest struct {
	Prompt             string  `json:"prompt"`
	ApacheScore        float64 `json:"apache_score"`
	LeukoGlycemicIndex float64 `json:"leuko_glycemic_index"`
	Prediction         float64 `json:"prediction"`
}

func ExplainHandler(db *sql.DB) gin.HandlerFunc {
	return func(c *gin.Context) {
		var req ExplainRequest
		if err := c.ShouldBindJSON(&req); err != nil {
			fmt.Println("[ERROR] Bind error:", err)
			c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid request body"})
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
			c.JSON(http.StatusInternalServerError, gin.H{"error": "OpenAI API failed"})
			return
		}
		explanation := resp.Choices[0].Message.Content

		res, err := db.Exec(`
			INSERT INTO patients (apache_score, leuko_glycemic_index, prediction)
			VALUES (?, ?, ?)`, req.ApacheScore, req.LeukoGlycemicIndex, req.Prediction)
		if err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to insert patient"})
			return
		}

		patientID, err := res.LastInsertId()
		if err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to get patient ID"})
			return
		}

		_, err = db.Exec(`
			INSERT INTO explanations (patient_id, explanation)
			VALUES (?, ?)`, patientID, explanation)
		if err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": "Failed to insert explanation"})
			return
		}

		c.JSON(http.StatusOK, gin.H{
			"patient_id":  patientID,
			"explanation": explanation,
		})
	}
}
