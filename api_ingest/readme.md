
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
 
* Create a Worflow using [workflow.yaml](workflow.yaml)
