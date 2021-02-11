package main

import (
	"github.com/gin-gonic/gin"
	"github.com/surgachsurgach/data_production_demo/goLang/internal/pkg/dbs"
	"github.com/surgachsurgach/data_production_demo/goLang/internal/app/controllers"
	"log"
	"net/http"
)

func main() {

	err := dbs.InitRedis()
	if err != nil {
		log.Fatal("Failed to initialize redis!")
		panic(err)
	}

	gin.SetMode(gin.ReleaseMode)

	r := gin.New()
	r.Use(gin.LoggerWithConfig(gin.LoggerConfig{
		SkipPaths: []string{"/api/ping"},
	}))

	r.Use(gin.Recovery())

	r.GET("/api/guestHouse/ranking/:category", controllers.ReadGuestHouseRanking)

	r.GET("/api/ping", func(c *gin.Context) {
		c.Status(http.StatusOK)
	})

	err = r.Run("0.0.0.0:8080")
	if err != nil {
		log.Fatal("Failed to listening at 0.0.0.0:8080!")
	}
}
