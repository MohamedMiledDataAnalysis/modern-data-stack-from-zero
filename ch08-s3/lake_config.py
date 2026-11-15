"""Chapter 8 — one place for the S3 settings used by every script.

Practice mode (default): talks to the moto emulator on localhost:5000.
Real AWS: set  MERIDIAN_S3_MODE=aws  and your own bucket name.
"""
import os

import boto3

MODE = os.environ.get('MERIDIAN_S3_MODE', 'local')
BUCKET = os.environ.get('MERIDIAN_BUCKET', 'meridian-lake-demo')
REGION = 'eu-west-2'                       # London


def s3_client():
    if MODE == 'aws':
        return boto3.client('s3', region_name=REGION)
    return boto3.client('s3', region_name=REGION,
                        endpoint_url='http://localhost:5000',
                        aws_access_key_id='testing',
                        aws_secret_access_key='testing')
