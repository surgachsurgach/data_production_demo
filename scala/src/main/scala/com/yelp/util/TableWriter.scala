package com.yelp.util

import org.apache.spark.sql.{DataFrameWriter, Dataset, Row, SaveMode}

object TableWriter {
  def getWriter(ds: Dataset[Row], saveMode: SaveMode = SaveMode.Overwrite): DataFrameWriter[Row] = {
    ds
      .write
      .mode(saveMode)
      .format("orc")
      .option("compression", "zlib")
  }
}
