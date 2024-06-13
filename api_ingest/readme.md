# Paginated API data ingestion into BigQuery

This sample code allow you to create an ingestion mechanism using Workflows, Cloud Functions and an auxiliary control table in BigQuery, to continuosly ingest data from a paginated API.

![img](api-ingest.png)

* Create BigQuery table for storing the data. Replace YOUR_DATASET_NAME
````sql
CREATE TABLE `YOUR_DATASET_NAME.api_data`
(
  a STRING,
  b STRING,
  c STRING
);
````

* Create BigQuery table for saving state. Replace YOUR_DATASET_NAME
````sql
CREATE TABLE `YOUR_DATASET_NAME.api_control`
(
  datetime TIMESTAMP,
  token STRING,
  records STRING
);
````

* Create a Cloud Function:
  * Use the file [requirements.txt](requirements.txt)
  * Use the file [main.py](main.py). Replace YOUR_PROJECT_NAME and YOUR_DATASET_NAME
  * Assign a Service account with permissions to read and write into your BQ tables
 
* Create a Worflow using [workflow.yaml](workflow.yaml)
    * Assign a Service account with permissions to invoke your Cloud Function
 
* Create a Cloud Scheduler to run continuosly every X amount of time your workflow
