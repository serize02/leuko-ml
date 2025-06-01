package openai

import (
	"github.com/sashabaranov/go-openai"
	"github.com/serize02/xai-server/config"
)

var Client *openai.Client

func InitClient() {
	apiKey := config.GetOpenAIKey()
	Client = openai.NewClient(apiKey)
}
