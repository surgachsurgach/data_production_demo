ThisBuild / organization := "com.yelp"
ThisBuild / scalaVersion := "2.12.10"
// ThisBuild / autoCompilerPlugins := true
ThisBuild / assemblyJarName := "hyesung-data-batch.jar"

val emrVersion = "6.0.0"
val sparkVersion = "2.4.4"
val javaVersion = "1.8.0_272"
val sbtVersion = "1.4.6"
val assemblyVersion = "0.15.0"

lazy val batch = (project in file("."))
  .settings(
    name := "data-batch",
    libraryDependencies ++= Seq(
      "org.postgresql" % "postgresql" % "42.2.18",
      "mysql" % "mysql-connector-java" % "8.0.22",
      "org.apache.httpcomponents" % "httpcore" % "4.4.14",
      "org.apache.httpcomponents" % "httpclient" % "4.5.13",
      "org.apache.spark" %% "spark-core" % sparkVersion % "provided",
      "org.apache.spark" %% "spark-hive" % sparkVersion % "provided",
      "org.apache.spark" %% "spark-sql" % sparkVersion % "provided",
      "org.apache.spark" %% "spark-yarn" % sparkVersion % "provided",
      "org.scalatest" %% "scalatest" % "3.2.3",
      "com.github.scopt" %% "scopt" % "4.0.0",
      "org.json4s" %% "json4s-jackson" % "3.6.10",
      "net.debasishg" %% "redisclient" % "3.30",
      "com.amazonaws" % "aws-java-sdk" % "1.11.880" % "provided",
      "com.typesafe.play" %% "play-json" % "2.9.1"),
    resolvers ++= Seq(
      "EMR Repository" at s"https://s3.ap-northeast-2.amazonaws.com/ap-northeast-2-emr-artifacts/$emrVersion/repos/maven/",
      Resolver.sonatypeRepo("public"),
      Resolver.typesafeRepo("releases")))

baseAssemblySettings

assemblyMergeStrategy in assembly := {
  case PathList("META-INF", _ @_) => MergeStrategy.discard
  case _ => MergeStrategy.last
}

assemblyOption in assembly := (assemblyOption in assembly).value.copy(includeScala = false)
