# Simple Data API for BigQuery

This is a simple demonstration of how to share data stored on BigQuiery implementing a Data API on Cloud Functions.

* [Learn how to Configure HTTPS triggers for Cloud Functions](https://cloud.google.com/functions/docs/calling/http#console).

This code exposes an entire dataset through the HTTPS endpoint. Consumers should provide the **table_name** query parameter along with an optional **table_record_id** to retrieve a specific record.

The structure of the request should be as follows:

GET https://**{your_region}**-**{your_project_id}**.cloudfunctions.net/**{your_function_name}**/**{table_name}**/**{table_record_id}**

* An example request to get the entire data available on table products would be https://**{your_region}**-**{your_project_id}**.cloudfunctions.net/**{your_function_name}**/**products**/

* An example request to get the Customer record with ID 1 would be https://**{your_region}**-**{your_project_id}**.cloudfunctions.net/**{your_function_name}**/**customers**/**1**


## Security considerations
* Consider that this code could be vulnerable againts common attacks such as SQL injection, use it carefully.
* Always review this demonstration code with your security and compliance team to find wheter you can use it as a basis or not not.
* This code is not intented for production, only a demonstration.
* When publishing an API to the internet, it is recommended to use an API Gateway, such as Apigee. Refer to the [Reference Architecture](https://cloud.google.com/api-gateway/docs/architecture-overview).
