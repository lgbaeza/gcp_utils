# Dataflow SQL Server to BigQuery
https://cloud.google.com/dataflow/docs/guides/templates/provided/sqlserver-to-bigquery

1. Create a Cloud SQL database within a VPC of yours
2. Ensure connectivity is setup: routing, firewall
3. Ensure APIs are enabled
4. Ensure Permissions networking (in case shared networks exist) are in order for both Worker Service Account and Dataflow service account
   * service-PROJECT_NUMBER@dataflow-service-producer-prod.iam.gserviceaccount.com - [Dataflow service account](https://cloud.google.com/dataflow/docs/concepts/security-and-permissions#df-service-account)
   * PROJECT_NUMBER-compute@developer.gserviceaccount.com - [Worker service account](https://cloud.google.com/dataflow/docs/concepts/security-and-permissions#worker-service-account)
5. Ensure Permissions for GCS, BQ Job User, and BQ Data Editor are in order for Worker Service Account Dataflow service account
   * PROJECT_NUMBER-compute@developer.gserviceaccount.com - [Worker service account](https://cloud.google.com/dataflow/docs/concepts/security-and-permissions#worker-service-account)
6. Create SQL Server source table according to [sample](/lgbaeza/mycloudstuff/blob/main/db/sqlserver_sample_transactions.sql)
7. Create BQ Dataset erp_sqlserver and table transactions:
````sql
-- ### Create equivalent BQ target Table
CREATE TABLE erp_sqlserver.transactions (
  tx_id INT64,
  tx_date DATE,
  amount FLOAT64
);
````
8. Create a GCS bucket
9. Launch job, replacing {}:
* {YOUR_REGION}
* {YOUR_PROJECT}
* {YOUR_CLOUD_SQL_PRIVATE_IP}
* {YOUR_REGION}
* {YOUR_SUBNETWORK_NAME}
* {YOUR_NETWORK_NAME}
* {YOUR_DB_NAME}
````bash
gcloud dataflow flex-template run sqlserver-to-bq \
--template-file-gcs-location gs://dataflow-templates-{YOUR_REGION}/latest/flex/SQLServer_to_BigQuery \
--region {YOUR_REGION} \
--worker-region {YOUR_REGION} \
--subnetwork projects/{YOUR_PROJECT}/regions/{YOUR_REGION}/subnetworks/{YOUR_SUBNETWORK_NAME} \
--network projects/{YOUR_PROJECT}/global/networks/{YOUR_NETWORK_NAME} \
--parameters "^~^connectionURL=jdbc:sqlserver://{YOUR_CLOUD_SQL_PRIVATE_IP}:1433;encrypt=true;trustServerCertificate=true;database={YOUR_DB_NAME}\
~username=dataflow\
~password=D4t4fl0w!\
~query=SELECT * FROM erp.dbo.transactions\
~outputTable={YOUR_PROJECT}:erp_sqlserver.transactions\
~bigQueryLoadingTemporaryDirectory=gs://{YOUR_PROJECT}/scratch/sqlserver_to_bq\
~useColumnAlias=false\
~isTruncate=false\
~fetchSize=50000\
~createDisposition=CREATE_NEVER\
~usePublicIps=false" \
--flexrs-goal=SPEED_OPTIMIZED
````

# Cautions
* This will generate cost in your account
* ;encrypt=true;trustServerCertificate=true is not intended for production
