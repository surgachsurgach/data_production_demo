# data-batch

Home for batch and data pipeline.

### Setup development environments
#### Python
- Recommend IDE: [PyCharm](https://www.jetbrains.com/ko-kr/pycharm/)
- Python version: [3.8.1](https://www.python.org/downloads/)  
- pip requirements: See `settings/requirements.txt`
- Lint
  - [isort](https://github.com/timothycrosley/isort)
    - Run with `isort`
  - [black](https://github.com/psf/black)
    - Run with `black -l 255 -t py38`
  - [flake8](http://flake8.pycqa.org/en/latest/)
    - See `./settings/lint/python/tox.ini` to check flake8 configurations
    - Run with `flake8 --config=tox.ini`
  - You can find the all packages in `pip`!
  - If you use PyCharm, you can register these lint tools into IDE to lint your file automatically.
    - Check `Preferences > Tools > File Watcher`
    - If it is too noisy, you just can register to `External Tools`
- Source root: `data-batch/python`

#### Scala
- Recommend IDE: [IntelliJ IDEA](https://www.jetbrains.com/ko-kr/idea/)
- Scala version: 2.12.10
- JDK version: [OpenJDK8 1.8.0_272](https://openjdk.java.net/install/)
  - Since Spark does not fully supports JDK9+, we will use JDK8 for now.
> Use homebrew to install `OpenJDK8`
```shell script
brew tap AdoptOpenJDK/openjdk
brew install adoptopenjdk-openjdk8
```
- [sbt](https://www.scala-sbt.org/) version: `1.4.6`
> Use homebrew to install `sbt`
```shell script
brew install sbt
```
- Source root: `data-batch/scala`
- Lint
  - [Scalafmt](https://scalameta.org/scalafmt/)
    - See `./settings/lint/scala/scalafmt.config` and apply it to your IDE such as IntelliJ.
  - [Scalastyle](http://www.scalastyle.org/)
    - See `./settings/lint/scala/scalastyle-config.xml` and apply it to your IDE such as IntelliJ.
      - You should copy that file to `./idea` in your directory in order to apply it to IntelliJ.
  - If you don't use IDE, you can manually run scalafmt/scalastyle through your CLI environment.
- Compile
  - ```shell script
    (at source root)
    > sbt compile assembly
    ```
  - Packaged artifact ([Fat JAR](http://tutorials.jenkov.com/maven/maven-build-fat-jar.html)) will be generated at `data-batch/scala/target/scala-2.12/croquis-data-batch.jar`

### Test your code changes
#### Python
We have [staging Airflow server](http://airflow-staging.data.zigzag.kr/) to test Airflow code changes. Commit and push your local changes on your branch and [deploy it to
staging server](http://jenkins.data.zigzag.kr/job/Service/job/Airflow/job/Deploy%20to%20staging/).

#### Scala
1. Build your code on local with `sbt compile assembly`.
2. Deploy an EMR cluster (See `python/util/emr/cluster.py`) with your own [PEM key](https://docs.aws.amazon.com/ko_kr/AWSEC2/latest/UserGuide/ec2-key-pairs.html).
It will be used when you connect to EMR cluster through `ssh`.
3. Transfer your local build result to EMR cluster using `scp`:
```shell script
scp -i {PEM_KEY_LOCATION} data-batch/scala/target/scala-2.12/croquis-data-batch.jar \ 
hadoop@{EMR_MASTER_HOST}:/home/hadoop/data-batch
```
4. Submit your job using `spark-submit`:
```shell script
spark-submit --master yarn --deploy-mode cluster --class \
com.croquis.main.scala.{YOUR_CLASS} croquis-data-batch.jar {PARAMS}
```
5. See job logs on EMR web console when an error occurred.

Or you can use [EMR Step](https://docs.aws.amazon.com/ko_kr/emr/latest/ReleaseGuide/emr-spark-submit-step.html) feature to test your Scala code on EMR cluster. In this case, you should upload your own JAR into [designated S3 location](https://s3.console.aws.amazon.com/s3/buckets/croquis-data-emr/application/?region=ap-northeast-2&tab=overview)
or build and upload it via [CodeBuild](https://ap-northeast-2.console.aws.amazon.com/codesuite/codebuild/projects/data-batch/history?region=ap-northeast-2).

### Make Pull Request
#### Code review
Basically, we review codes through the PR for every single change. `In code review, we will focus on the contents of PR or somewhat greater,
rather than the code style or convention.` That's the reason why we implements multiple formatters/linters.

#### Apply lint
So your code changes must pass all lint tools. Also if you want to change lint rules, please suggest freely!

### Deploy
#### Python
We use Jenkins to deploy Python code to Airflow container, which uses Python code in production. Please refer [here](http://jenkins.data.zigzag.kr/job/Service/job/Airflow/job/Deploy%20container/).

#### Scala
Currently we use [CodeBuild](https://ap-northeast-2.console.aws.amazon.com/codesuite/codebuild/projects/data-batch/history?region=ap-northeast-2) and [S3](https://s3.console.aws.amazon.com/s3/buckets/croquis-data-emr/application/production/?region=ap-northeast-2&tab=overview) to
deploy Scala/Spark code in form of fat JAR. EMR step will reference S3 path and deliever it to EMR clusters.

### Additional settings
#### Set proxy to see Spark logs located on core node
See [here](https://docs.aws.amazon.com/ko_kr/emr/latest/ManagementGuide/emr-ssh-tunnel-local.html) why you would need this settings.

1. Install `FoxyProxy` on your browser. it currently supports [Chrome](https://chrome.google.com/webstore/search/foxy%20proxy) and Firefox.
2. Choose `Import/Export` tab and import settings on this repository at `settings/foxyproxy-settings.xml`
3. Connect your EMR master node through `ssh` with option `-d`. `python/util/emr/cluster.py` will provide proper `ssh` command in default.
4. Now you can access to core node's YARN and it's logs through SSH tunneling and proxy settings.
