-- Luis Gerardo Baeza

-- History of column quality
Create or replace view dataplex_scan_results.vw_quality_column_history as
  SELECT 
    data_quality_scan.data_scan_id,
    data_quality_job_id,
    job_end_time,

    data_source.table_project_id,
    data_source.dataset_id,
    data_source.table_id,
    
    data_quality_job_configuration.sampling_percent,
    rule_type,
    rule_column,
    
    rule_dimension,
    rule_rows_passed_percent,
    job_quality_result.passed,
    job_quality_result.score
  FROM `dataplex_scan_results.quality`; 

-- Snapshot of column quality
Create or replace view dataplex_scan_results.vw_quality_column_snapshot as
  SELECT 
  data_quality_scan.data_scan_id,
  data_quality_job_id,
  job_end_time,

  data_source.table_project_id,
  data_source.dataset_id,
  data_source.table_id,
  
  data_quality_job_configuration.sampling_percent,
  rule_type,
  rule_column,
  
  rule_dimension,
  rule_rows_passed_percent,
  job_quality_result.passed,
  job_quality_result.score

  FROM `dataplex_scan_results.quality` as t

where 
 t.data_quality_job_id = (
        SELECT
            data_quality_job_id
        FROM
            `dataplex_scan_results.quality`
        ORDER BY
            job_end_time DESC
        LIMIT 1
    )


-- job run history
create or replace view `dataplex_scan_results.vw_quality_job_history`  as

    SELECT 
        data_quality_job_id,
        data_quality_scan.project_id,
        data_quality_scan.location,
        data_quality_scan.data_scan_id,
        job_start_time,
        job_end_time,
        DATETIME_DIFF(datetime(job_end_time),datetime(job_start_time),SECOND) as duration_sec

    FROM `dataplex_scan_results.quality` 
    group by 1,2,3,4,5,6
