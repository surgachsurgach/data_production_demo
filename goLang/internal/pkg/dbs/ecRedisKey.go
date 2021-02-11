package dbs

import (
	"bytes"
)

const (
	KEY_RANKING_BRANDS           = "guest_house:ranking"
)

func GetGuestHouseRankingsKey(category string) string {
	var b bytes.Buffer
	b.WriteString(KEY_RANKING_BRANDS)
	b.WriteString(":")
	b.WriteString(category)

	return b.String()
}