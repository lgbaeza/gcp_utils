import urllib

import google.auth.transport.requests
import google.oauth2.id_token

REGION = "YOUR_REGION"
PROJECT_ID = "YOUR_PROJECT
FUNCTION_NAME = "data-api" #Reeplace with your function name

def make_authorized_get_request(endpoint, audience):
    """
    make_authorized_get_request makes a GET request to the specified HTTP endpoint
    by authenticating with the ID token obtained from the google-auth client library
    using the specified audience value.
    """

    # Cloud Functions uses your function's URL as the `audience` value
    # audience = https://project-region-projectid.cloudfunctions.net/myFunction
    # For Cloud Functions, `endpoint` and `audience` should be equal

    req = urllib.request.Request(endpoint)

    auth_req = google.auth.transport.requests.Request()
    id_token = google.oauth2.id_token.fetch_id_token(auth_req, audience)

    return id_token

    #req.add_header("Authorization", f"Bearer {id_token}")
    #response = urllib.request.urlopen(req)
    
    #return response.read()

endpoint = f"https://{REGION}-{PROJECT_ID}.cloudfunctions.net/{FUNCTION_NAME}"
print(make_authorized_get_request(endpoint,endpoint))
