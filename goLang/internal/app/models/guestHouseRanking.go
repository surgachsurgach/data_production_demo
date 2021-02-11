package models

import (
	"encoding/json"
	"github.com/data_production_demo/goLang/internal/pkg/dbs"
	"log"
)

type GuestHouseRanking struct {
	BusinessIDs  []string `json:"business_ids, list"`
}

func ReadGuestHouseRanking(category string) (GuestHouseRanking, error) {
	ranking := GuestHouseRanking{}
	key := dbs.GetGuestHouseRankingsKey(category)

	rankingStr, err := dbs.RedisGet(key)
	if err != nil || rankingStr == "" {
		return ranking, err
	}

	err = json.Unmarshal([]byte(rankingStr), &ranking)
	if err != nil {
		log.Println(err.Error())
		return ranking, err
	}

	return ranking, nil
}
