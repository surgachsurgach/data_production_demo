package com.yelp.core.spark

import scala.util.Random

import org.apache.spark.{SparkConf, SparkContext}
import org.apache.spark.sql.{Dataset, SparkSession}

class ExtendedSparkContext {
  private val sparkConf = new SparkConf()
  private val sparkSession = new SparkSession.Builder()
    .config(sparkConf)
    .enableHiveSupport()
  val MAIN_BUCKET_URI = "s3://croquis-data-emr"
  val LOG_WAREHOUSE_URI = "s3://logs.data.zigzag.kr"

  val spark: SparkSession = sparkSession.getOrCreate()
  val sc: SparkContext = spark.sparkContext

  def isTableExist(database: String, table: String): Boolean = spark.catalog.tableExists(database, table)
}

object ExtendedSparkContext {
  implicit class RegisterableDataset[T](ds: Dataset[T]) {
    def register: String = {
      val tableName = Random.alphanumeric.take(10).mkString.toLowerCase
      ds.createOrReplaceTempView(tableName)

      tableName
    }
  }
}
