package dbs

import (
	"context"
	"errors"
	"fmt"
	"github.com/go-redis/redis/v8"
	"log"
	"time"
)

const (
	MAX_RETRIES = 10
)

var (
	ctx    = context.Background()
	reader *redis.Client
)

func makeConnection(address string) (*redis.Client, error) {
	var client *redis.Client
	for i := 0; i < MAX_RETRIES; i++ {
		client = redis.NewClient(&redis.Options{
			Addr:     address,
			Password: "",
			DB:       0,
		})

		_, err := client.Ping(ctx).Result()
		if err == nil {
			return client, nil
		} else {
			log.Println(err.Error())
		}

		time.Sleep(time.Second * 1)
	}

	return nil, errors.New(fmt.Sprintf("Failed to make connection with %s!", address))
}

func InitRedis() error {
	var err error
	err = nil

	readerAddr := "redis cluster address here.."

	reader, err = makeConnection(readerAddr)
	if err != nil {
		log.Println(err.Error())
		return err
	}

	return nil
}

func RedisGet(key string) (string, error) {
	val, err := reader.Get(ctx, key).Result()
	if err != nil {
		if err == redis.Nil {
			return "", nil
		} else {
			log.Println(err.Error())
			return "", err
		}
	}

	return val, nil
}
