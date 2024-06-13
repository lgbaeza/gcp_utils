# Sample code to be orchestrated by Workflows. Make sure to adapt to your own data schema and test it
# @lgbaeza June 2024
# Replace YOUR_PROJECT_ID
# Replace YOUR_DATASET_NAME
# Adjust table_data and table_control as needed

import functions_framework
from datetime import datetime
from google.cloud import bigquery
import json

project_id = "YOUR_PROJECT_ID"
dataset = "YOUR_DATASET_NAME"
table_data = "api_data"
table_control = "api_control"
client = bigquery.Client(project=project_id)

def run_bq_query(sql_query):
    query_job = client.query(sql_query)
    rows = query_job.result()
    data = [dict(row) for row in rows]
    return data

def make_request_api(token=None):
    if token is None:
        return 1, ("a", "b", "c")
    else:
        return int(token) + 1, ("a", "b", "c")

@functions_framework.http
def hello_http(request):

    request_args = request.get_json()
    print(request_args)
    step_type = request_args.get("step_type")

    # Get current status
    if step_type == "GET_TOKEN":
        sql_query = f"""
            BEGIN TRANSACTION;
                SELECT token FROM {dataset}.{table_control} ORDER BY `datetime` DESC LIMIT 1;
            COMMIT TRANSACTION;
        """
        token_data = run_bq_query(sql_query)
        curr_token = 1 if token_data == [] else int(token_data[0]["token"])
        
        return str(curr_token)
    
    # Request and save data
    elif step_type == "GET_DATA":
        curr_token = request_args.get("curr_token")
        new_token, data = make_request_api(curr_token)

        sql_query = f"INSERT INTO {dataset}.{table_data} (a, b, c) VALUES {data}"
        run_bq_query(sql_query)

        return json.dumps({
            "new_token": new_token,
            "records": len([data]), # Modify
            "datetime_col": str(datetime.now().replace(microsecond=0))
        })

    # Save status
    elif step_type == "SAVE_STATUS":
        new_token = request_args.get("new_token")
        records = request_args.get("records")
        datetime_col = request_args.get("datetime_col")
        sql_query = f"""
            BEGIN TRANSACTION;
                INSERT INTO {dataset}.{table_control} (`datetime`, `token`, `records`) 
                    VALUES ('{datetime_col}', '{new_token}', '{records}');
            COMMIT TRANSACTION;
                """
        run_bq_query(sql_query)

        return f'{records} records processed.'
    
    else:
        return ''

