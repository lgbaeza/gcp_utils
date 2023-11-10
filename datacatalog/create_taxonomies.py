# install
# pip install google-cloud-datacatalog
# pip install --upgrade google-api-core

# Imports
from google.cloud import datacatalog_v1
from google.api_core.client_options import ClientOptions
from google.cloud.datacatalog_v1.types import *
import time

# Constants
PROJECT = "YOUR_PROJECT_ID"
taxonomies = ["TX1", "TX2", "TX3", "TX4"]
tags = "YOUR_TAG_PREFIX"
tagdepth = 5 # Number of tags per taxonomy
taglength = 10 # Number of subtags
api_location = "" # E.g. us-west1-
endpoint = f"{api_location}datacatalog.googleapis.com"

client_opts = ClientOptions(api_endpoint=endpoint)
client = datacatalog_v1.PolicyTagManagerClient(client_options=client_opts)
parent = f"projects/{PROJECT}/locations/us"

# List taxonomies
def sample_list_taxonomies():
    page_result = client.list_taxonomies(parent=parent)

    for response in page_result:
        print(response)

# Create taxonomies
def create_taxonomies():
    
    for taxonomy_name in taxonomies:
        taxonomy = Taxonomy(display_name=taxonomy_name)
        tax_response = client.create_taxonomy(parent=parent, taxonomy=taxonomy)
        tax_resource = tax_response.name
        print(f"Taxonomy {tax_resource} created")

        for x in range(1, tagdepth + 1):
            tag_name = f"{tags}-{x}"
            policy_tag = PolicyTag(display_name=tag_name)
            pt_response = client.create_policy_tag(parent=tax_resource, policy_tag=policy_tag)
            pt_resource = pt_response.name

            for y in range(1, taglength + 1):
                tag_name = f"{tags}-{x}-{y}"
                policy_subtag = PolicyTag(display_name=tag_name, parent_policy_tag=pt_resource)
                pst_response = client.create_policy_tag(parent=tax_resource, policy_tag=policy_subtag)
                pst_resource = pst_response.name

        print(f"Created tag hierarchy for {tax_resource}")
        time.sleep(10)

def main():
    create_taxonomies()

if __name__ == "__main__":
  main()
