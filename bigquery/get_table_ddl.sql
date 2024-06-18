-- Retrieve the DDL for a table or view
SELECT
 ddl
FROM
 {YOUR_DATASET_ID}.INFORMATION_SCHEMA.TABLES
WHERE
 table_name="YOUR_TABLE_NAME"
