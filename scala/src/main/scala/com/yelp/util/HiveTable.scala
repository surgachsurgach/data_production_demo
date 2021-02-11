package com.yelp.util

import com.yelp.core.spark.ExtendedSparkContext

import org.apache.spark.sql.{Dataset, Row, SaveMode}

class HiveTable(database: String, table: String) {
  def save(ds: Dataset[Row], saveMode: SaveMode = SaveMode.Overwrite)(implicit xsc: ExtendedSparkContext): Unit = {
    val writer = TableWriter.getWriter(ds, saveMode)
    if (xsc.isTableExist(database, table)) writer.insertInto(s"$database.$table")
    else writer.saveAsTable(s"$database.$table")
  }

  def loadAsTable()(implicit xsc: ExtendedSparkContext): String = {
    import xsc.spark
    spark.sql(s"""
       |SELECT * FROM $database.$table
      """.stripMargin)
      .createOrReplaceTempView(table)

    table
  }

  def load()(implicit xsc: ExtendedSparkContext): Dataset[Row] = {
    import xsc.spark
    spark.sql(s"""
       |SELECT * FROM $database.$table
      """.stripMargin)
  }
}
