package com.yelp.batch.mart.guestHouse.app

import java.time.LocalDate
import java.time.format.DateTimeFormatter

import com.yelp.batch.mart.guestHouse.table.{RANKING_DELIVERY, RANKING_MONTHLY, RANKING_WEEKLY, RANKING_YEARLY}
import com.yelp.core.spark.ExtendedSparkContext
import com.yelp.core.spark.ExtendedSparkContext._

import org.apache.spark.sql.functions.typedLit

object BuildGuestHouseRankingDelivery {
  def main(args: Array[String]): Unit = {
    implicit val xsc: ExtendedSparkContext = new ExtendedSparkContext()
    import xsc.spark
    import spark.implicits._

    val date: LocalDate = LocalDate.parse(args(0), DateTimeFormatter.ofPattern("yyyy-MM-dd"))

    val rankingWeekly = RANKING_WEEKLY.load().withColumn("category", typedLit[String]("weekly")).register
    val rankingMonthly = RANKING_MONTHLY.load().withColumn("category", typedLit[String]("monthly")).register
    val rankingYearly = RANKING_YEARLY.load().withColumn("category", typedLit[String]("yearly")).register

    val rankingDeliveryDS = spark.sql(
      s"""
         |(SELECT * FROM $rankingWeekly)
         | UNION (SELECT * FROM $rankingMonthly)
         | UNION (SELECT * FROM $rankingYearly)
         |""".stripMargin)
      .as[RankingPerCategory]
      .groupByKey(_.category)
      .mapGroups {
        case(category, rankings) =>
          val businessIDs = rankings.toList.sortBy(_.ranking).map(_.business_id).mkString(",")
          RankingDelivery(category, s"[$businessIDs]")
      }
      .withColumn("stamp_date", typedLit[String](date.toString))

    RANKING_DELIVERY.save(rankingDeliveryDS)
  }
}

case class RankingPerCategory(category: String, business_id: String, ranking: Int)
case class RankingDelivery(category: String, business_ids: String)
