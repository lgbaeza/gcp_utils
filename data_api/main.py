import functions_framework
import re, json
from datetime import datetime
from cors import cors_enabled_function
from google.cloud import bigquery
from datetime import datetime
from geolocation import get_geolocation
from google.cloud.bigquery.job import QueryJobConfig

bigquery_project_id = "YOUR_PROJECT_ID"
bigquery_dataset = "YOUR_BQ_DATASET"
bigquery_analytcs_table_id = f"{bigquery_project_id}.{bigquery_dataset}.analytics_source_ip"
client_bq = bigquery.Client()
analytics_info = {
    "datetime": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    "source_ip": "",
    "entity": "",
    "method": "",
    "success": "false"
}

def save_request_info(row):
    res = client_bq.insert_rows_json(bigquery_analytcs_table_id, [row])
    print(res)

@functions_framework.http
def hello_http(request):    
    result = {}
    
    try:
        remote_addr = request.environ["HTTP_X_FORWARDED_FOR"].split(",")[0]
        country_name, state, latitude, longitude = get_geolocation(remote_addr)
        analytics_info["source_ip"] = remote_addr
        analytics_info["country_name"] = country_name
        analytics_info["state"] = state
        analytics_info["latitude"] = latitude
        analytics_info["longitude"] = longitude
    except:
        pass

    headers, cors_request = cors_enabled_function(request)
    request_args = request.args
    if cors_request:
        return (result, 204, headers)

    try:
        entity = request.path.split("/")[1]
        analytics_info["entity"] = entity
        try:
            entity_id = request.path.split("/")[2]
        except:
            entity_id = None

        analytics_info["method"] = request.method
        if request.method == "GET":
            bq_query_condition = False
            bq_query = f"""
                SELECT * FROM {bigquery_dataset}.{entity} 
            """
            if entity_id is None:
                result = []
            else:
                bq_query += f" WHERE {entity}_id = '{entity_id}'"
                bq_query_condition = True

            if request_args is not None:
                for param in request_args:
                    param_value = request_args.get(param)

                    bq_query += (" AND " if bq_query_condition else " WHERE ") \
                                + f" LOWER({param}) like LOWER('%{param_value}%')"

            print(bq_query)

            job_config = QueryJobConfig(use_query_cache=False)
            for row in client_bq.query(query = bq_query, job_config = job_config):
                row_object = {}
                for column in row.keys():
                    row_object[column] = row.get(column)
                
                if entity_id is None:
                    result.append(row_object)
                else:
                    result = row_object

        analytics_info["success"] = "true"
    
    except Exception as e:
        print(e)
        
    finally:
        print("saving analytics...")
        print(analytics_info)
        save_request_info(analytics_info)
        return (result, 200, headers)
