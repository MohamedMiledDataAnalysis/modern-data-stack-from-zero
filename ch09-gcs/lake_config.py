"""Chapter 9 — one place for the Cloud Storage settings used by every script.

Practice mode (default): talks to the fake-gcs-server emulator on localhost:4443.
Real Google Cloud: set  MERIDIAN_GCS_MODE=gcp, MERIDIAN_GCP_PROJECT and MERIDIAN_BUCKET.
"""
import os

from google.auth.credentials import AnonymousCredentials
from google.cloud import storage

MODE = os.environ.get('MERIDIAN_GCS_MODE', 'local')
BUCKET = os.environ.get('MERIDIAN_BUCKET', 'meridian-lake-demo')
PROJECT = os.environ.get('MERIDIAN_GCP_PROJECT', 'meridian-local')
LOCATION = 'europe-west2'                  # London


def gcs_client():
    if MODE == 'gcp':
        return storage.Client(project=PROJECT)
    return storage.Client(project=PROJECT, credentials=AnonymousCredentials(),
                          client_options={'api_endpoint': 'http://localhost:4443'})
