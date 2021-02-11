package com.yelp.batch.mart.guestHouse.app

import com.yelp.batch.mart.guestHouse.table.{BUSINESS, REVIEWS, TIPS}
import com.yelp.core.spark.ExtendedSparkContext

object ConvertJsonToHiveTable {
  def main(args: Array[String]): Unit = {
    implicit val xsc: ExtendedSparkContext = new ExtendedSparkContext()
    import xsc.spark

    val tipsDS = spark.read.format("json").load("s3://yelp/yelp_academic_dataset_review.json")
    val reviewsDS = spark.read.format("json").load("s3://yelp/yelp_academic_dataset_tip.json")
    val businessDS = spark.read.format("json").load("s3://yelp/yelp_academic_dataset_business.json")

    BUSINESS.save(businessDS)
    REVIEWS.save(reviewsDS)
    TIPS.save(tipsDS)

  }
}
