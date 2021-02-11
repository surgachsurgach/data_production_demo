package com.yelp.batch.mart.guestHouse.app

import java.time.LocalDate
import java.time.format.DateTimeFormatter

import com.yelp.batch.mart.guestHouse.table.RANKING_YEARLY
import com.yelp.core.spark.ExtendedSparkContext

import org.apache.spark.sql.functions.typedLit

object GuestHouseRankingYearly {
  def main(args: Array[String]): Unit = {
    implicit val xsc: ExtendedSparkContext = new ExtendedSparkContext()

    val date: LocalDate = LocalDate.parse(args(0), DateTimeFormatter.ofPattern("yyyy-MM-dd"))
    val toDate = date
    val fromDate = date.withDayOfYear(1)

    val rankingDailyDS = CalculateGuestHouseRankingHelper.calculate(fromDate, toDate)
      .withColumn("stamp_date", typedLit[String](date.toString))

    RANKING_YEARLY.save(rankingDailyDS)
  }
}
