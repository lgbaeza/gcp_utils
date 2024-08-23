### Monitor latest queries (UTC)
SELECT
  EXTRACT(DATE FROM  creation_time) day,
  EXTRACT(HOUR FROM  creation_time) hour,
  sum(total_bytes_billed)/1000000000 gb_scanned
FROM
  `region-us`.INFORMATION_SCHEMA.JOBS_BY_PROJECT
WHERE
  extract(DATE from creation_time) >= DATE_SUB(CURRENT_DATE(), INTERVAL 1 DAY)
GROUP BY 1,2
ORDER BY 1 desc, 2 desc;


### Monitor last queries in local time
SELECT
  EXTRACT(DATE FROM  timestamp(DATETIME(creation_time, 'America/Santiago'))) date,
  EXTRACT(HOUR FROM  timestamp(DATETIME(creation_time, 'America/Santiago'))) hour,
  EXTRACT(MINUTE FROM  timestamp(DATETIME(creation_time, 'America/Santiago'))) minute,
  sum(total_bytes_billed)/1000000000 gb_scanned
FROM
  `region-us`.INFORMATION_SCHEMA.JOBS_BY_PROJECT
WHERE
  extract(DATE from creation_time) >= DATE_SUB(CURRENT_DATE(), INTERVAL 1 DAY)
GROUP BY 1,2,3
ORDER BY 1 desc, 2 desc, 3 desc;






