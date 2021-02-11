# data-production-demo by hyesungOh
- yelp dataset을 이용하여 전체 지역을 대상으로 guest house ranking table을 생성합니다.
- 프로젝트에 사용한 테이블: review.json, tips.json, business.json
- TODOs
  - 국가별 또는 지역별 ranking

#### Project Architecture
- `data_production_diagram_HyesungOh.pdf`를 참고해주세요 

#### Python(Airflow)
- Source root: `data_production_demo/python`
- `Apache Airflow`: https://airflow.apache.org/docs/apache-airflow/stable/index.html
- DAG/Operator
  - `create_emr_cluster`
    - boto3 client를 이용해 AWS EMR Cluster를 띄웁니다. 
  - `build_guest_house_ranking_tables`
    - guest_house_ranking_weekly, guest_house_ranking_monthly, guest_house_ranking_yearly 데이터를 빌드하고 하이브 테이블로 적재하는 batch-job을 scheduling 합니다.
  - `upload_guest_house_ranking_to_ec`
    - 주별, 월별, 년별 게스트하우스 랭킹 데이터를 REST API로 서빙하기 위해 ElasticCache에 업로드합니다.

#### Scala(Spark)
- Source root: `data_production_demo/scala`
- `Apache Spark quick start`: https://spark.apache.org/docs/latest/quick-start.html 
- guest_house_ranking_weekly, guest_house_ranking_monthly, guest_house_ranking_yearly, guest_house_ranking_delivery 테이블 빌드 및 하이브 테이블 적재

#### Golang(REST API)
- Source root: `data_production_demo/goLang`
- 게스트 하우스 랭킹 데이터를 category별로 서빙합니다.
- webframework
  - `gin`: https://github.com/gin-gonic/gin

