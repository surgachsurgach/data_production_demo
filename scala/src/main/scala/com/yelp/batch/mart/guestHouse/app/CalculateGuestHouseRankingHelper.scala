package com.yelp.batch.mart.guestHouse.app

import java.time.LocalDate

import com.yelp.batch.mart.guestHouse.table.{BUSINESS, REVIEWS, TIPS}
import com.yelp.core.spark.ExtendedSparkContext

import org.apache.spark.sql.{Dataset, Row}
import org.apache.spark.sql.expressions.Window
import org.apache.spark.sql.functions.{asc, desc, rank}

object CalculateGuestHouseRankingHelper {
  def calculate(from: LocalDate, to: LocalDate)(implicit xsc: ExtendedSparkContext): Dataset[Row] = {
    import xsc.spark
    import spark.implicits._

    val business = BUSINESS.loadAsTable()
    val tips = TIPS.loadAsTable()
    val reviews = REVIEWS.loadAsTable()

    val guestHouseDS = spark.sql(s"""
          |SELECT
          | business_id,
          | name,
          | address,
          | CAST(is_open AS INT) as is_open,
          | CAST(state AS INT) as state
          |FROM $business
          | WHERE categories like "%Hotels & Travel%" and categories like "%Guest Houses%"
          |""".stripMargin)
      .as[GuestHouse]

    val tipScoreDS = spark.sql(s"""
          |SELECT
          | DATE_FORMAT(CAST(date AS TIMESTAMP), "yyyy-MM-dd") AS access_date,
          | business_id,
          | CAST(cool AS INT) AS cool,
          | CAST(funny AS INT) AS funny,
          | CAST(stars AS INT) AS stars,
          | CAST(useful AS INT) as useful,
          | text AS review
          |FROM $tips
          |WHERE TO_DATE(FROM_UTC_TIMESTAMP(CAST(date AS TIMESTAMP), "Asia/Seoul")) BETWEEN "${from.toString}" AND "${to.toString}"
          |""".stripMargin)
      .as[Tips]
      .groupByKey(_.business_id)
      .mapGroups {
        case(business_id, tipIter) =>
          val tipList = tipIter.toList
          val totalCount = tipList.length.toFloat

          // score = total sum of cool, useful, star, funny / total count of review
          val score = (tipList.map(tip => Array(tip.cool, tip.useful, tip.stars, tip.funny).sum).sum / totalCount)
          Score(business_id, score)
      }

    val reviewScoreDS = spark.sql(s"""
         |SELECT
         | DATE_FORMAT(CAST(date AS TIMESTAMP), "yyyy-MM-dd") AS access_date,
         | business_id,
         | CAST(compliment_count AS INT) AS compliment_count,
         | text AS review
         |FROM $reviews
         |WHERE TO_DATE(FROM_UTC_TIMESTAMP(CAST(date AS TIMESTAMP), "Asia/Seoul")) BETWEEN "${from.toString}" AND "${to.toString}"
         |""".stripMargin)
      .as[Reviews]
      .groupByKey(_.business_id)
      .mapGroups {
        case(business_id, reviewIter) =>
          val reviewList = reviewIter.toList
          val totalCount = reviewList.length.toFloat

          val score = reviewList.map(_.compliment_count).sum / totalCount
          Score(business_id, score)
      }

    val guestHouseScoreDS = tipScoreDS
      .union(reviewScoreDS)
      .groupByKey(_.business_id)
      .mapGroups {
        case(id, scores) => Score(id, scores.toList.map(_.score).sum)
      }


    val rankingAddedDS = guestHouseDS
      .joinWith(guestHouseScoreDS, guestHouseDS("business_id") === guestHouseScoreDS("business_id"), "left_outer")
      .map {
        case(guestHouse, null) => Score(guestHouse.business_id, 0)
        case(guestHouse, score) => Score(guestHouse.business_id, score.score)
      }
      .withColumn("ranking", rank.over(Window.orderBy(desc("total_score"))))
      .orderBy(asc("ranking"))

    rankingAddedDS
  }
}

case class GuestHouse(business_id: String, name: String, address: String, is_open: Int, state: String)
case class Tips(access_date: String, business_id: String, cool: Int, funny: Int, stars: Int, useful: Int, review: String)
case class Reviews(access_date: String, business_id: String, compliment_count: Int, review: String)
case class Score(business_id: String, score: Float)