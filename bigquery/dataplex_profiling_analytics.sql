-- history of column profile
CREATE VIEW `dataplex_scan_results.vw_profiling_column_history` AS 
    SELECT 
        data_source.dataplex_lake_id,
        data_source.dataplex_zone_id,
        data_source.dataset_id,
        data_source.table_project_id,
        column_name,
        column_type,
        data_profile_job_configuration.sampling_percent,

        percent_null, 
        percent_unique, 
        min_string_length, 
        max_string_length, 
        average_string_length,

        min_value,
        max_value,
        average_value,

        standard_deviation, 
        quartile_lower,
        quartile_median, 
        quartile_upper
    FROM `dataplex_scan_results.profiling`;

-- current snapshot of column profile
SELECT
    data_profile_job_id,
        job_end_time,
        data_source.dataplex_lake_id,
        data_source.dataplex_zone_id,
        data_source.dataset_id,
        data_source.table_project_id,
        column_name,
        column_type,
        data_profile_job_configuration.sampling_percent,

        percent_null, 
        percent_unique, 
        min_string_length, 
        max_string_length, 
        average_string_length,

        min_value,
        max_value,
        average_value,

        standard_deviation, 
        quartile_lower,
        quartile_median, 
        quartile_upper
  FROM
    `dataplex_scan_results.profiling` AS t
  WHERE t.data_profile_job_id = (
    SELECT
        data_profile_job_id
      FROM
        `dataplex_scan_results.profiling`
      ORDER BY
        job_end_time DESC
      LIMIT 1
  )



-- job run history
create or replace view `dataplex_scan_results.vw_profiling_job_history`  as

    SELECT 
        data_profile_job_id,
        data_profile_scan.project_id,
        data_profile_scan.location,
        data_profile_scan.data_scan_id,
        job_start_time,
        job_end_time,
        DATETIME_DIFF(datetime(job_end_time),datetime(job_start_time),SECOND) as duration_sec

    FROM `dataplex_scan_results.profiling` 
    group by 1,2,3,4,5,6
