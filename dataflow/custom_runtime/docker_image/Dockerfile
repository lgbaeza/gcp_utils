# Stage 1: Base image
FROM python:3.10-slim as base

# Install Apache Beam SDK and other dependencies
RUN pip install --no-cache-dir \
    apache-beam[gcp]==2.58.1 \
    pydantic==2.9.0 \
    google-cloud-storage==2.18.0 \
    six==1.16.0

RUN pip check

ENV RUN_PYTHON_SDK_IN_DEFAULT_ENVIRONMENT=1

# Copy files from the official SDK image, including script/dependencies
COPY --from=apache/beam_python3.10_sdk:2.58.1 /opt/apache/beam /opt/apache/beam

# Set the entrypoint to Apache Beam SDK launcher
ENTRYPOINT ["/opt/apache/beam/boot"]
