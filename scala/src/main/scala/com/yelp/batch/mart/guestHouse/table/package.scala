package com.yelp.batch.mart.guestHouse

import com.yelp.util.HiveTable

package object table {
  val TIPS = new HiveTable("yelp", "tips_partitioned")
  val REVIEWS = new HiveTable("yelp", "reviews_partitioned")
  val BUSINESS = new HiveTable("yelp", "business_partitioned")
  val RANKING_WEEKLY = new HiveTable("guest_house", "ranking_weekly_partitioned")
  val RANKING_MONTHLY = new HiveTable("guest_house", "ranking_monthly_partitioned")
  val RANKING_YEARLY = new HiveTable("guest_house", "ranking_yearly_partitioned")
  val RANKING_DELIVERY = new HiveTable("guest_house", "ranking_delivery_partitioned")
}
