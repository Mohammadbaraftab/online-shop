# test_s3_connection.py

import boto3
from botocore.exceptions import NoCredentialsError

s3 = boto3.resource(
    's3',
    endpoint_url="https://s3.ir-thr-at1.arvanstorage.ir",  # Ensure https:// prefix
    aws_access_key_id="c4025bd2-049f-4124-a0bf-b5801bb5ef1f",
    aws_secret_access_key="34d37be8ac7147202b25eeb363c01227904392688e12989317909a2c3ec0f830",
    region_name="us-east-1"  # Adjust this to the correct region if needed
)

try:
    for bucket in s3.buckets.all():
        print(bucket.name)
except NoCredentialsError:
    print("Credentials not available.")
