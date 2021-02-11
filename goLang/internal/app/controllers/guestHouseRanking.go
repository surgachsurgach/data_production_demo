package controllers

import (
	"github.com/gin-gonic/gin"
	"net/http"
	"github.com/surgachsurgach/data_production_demo/goLang/internal/app/models"
)

func ReadGuestHouseRanking(c *gin.Context) {
	category := c.Param("category")
	if category == (string)(nil) {
		c.JSON(http.StatusBadRequest, gin.H{"message": "wrong category"})
		return
	}

	ranking, err := models.ReadGuestHouseRanking(category)
	if err != nil {
		c.JSON(http.StatusInternalServerError, gin.H{"message": err.Error()})
		return
	}

	c.JSON(http.StatusOK, ranking)
}
