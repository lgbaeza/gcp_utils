# Run a dataflow pipeline with custom container image

Official resources:
* [Use custom containers in Dataflow Documentation](https://cloud.google.com/dataflow/docs/guides/using-custom-containers)
* [List of sample custom container images for Dataflow](https://github.com/GoogleCloudPlatform/python-docs-samples/tree/main/dataflow/custom-containers)

### 1. Edit docker_image/Dockerfile with your runtime needs

### 2. Authenticate

```sh
gcloud auth application-default login
```

### 3. build the image using cloudbuild
```sh
cd docker_image
export BUCKET="YOUR_BUCKET"
export PROJECT="YOUR_PROJECT"
export IMAGE=gcr.io/$PROJECT/samples/dataflow/slim:1

# Build the image
gcloud builds submit .  --tag=$IMAGE
```

### 4. Upload the sample file to your bucket
```sh
gsutil cp kinlear_short.txt "gs://$BUCKET/dataflow_samples/"
```
### 5. Submit the job: 
    * To run locally: runner=DirectRunner
    * To run in Dataflow runner=DataflowRunner
```sh
export RUNNER=DataflowRunner

python3 main.py \
    --region us-central1 \
    --output "gs://$BUCKET/results/outputs" \
    --input "gs://$BUCKET/dataflow_samples/kinlear_short.txt" \
    --temp_location "gs://$BUCKET/tmp/"" \
    --runner $RUNNER \
    --project $PROJECT \
    --sdk_container_image $IMAGE \
    --job_name word-counter-custom-img
```
