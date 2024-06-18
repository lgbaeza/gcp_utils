-- Retrieve the DDL for a table or view
-- Luis Gerardo Baeza, 18 Jun 2024
SELECT
 ddl
FROM
 {YOUR_DATASET_ID}.INFORMATION_SCHEMA.TABLES
WHERE
 table_name="YOUR_TABLE_NAME"
