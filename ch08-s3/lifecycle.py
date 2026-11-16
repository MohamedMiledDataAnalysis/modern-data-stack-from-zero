"""Chapter 8, Step 5 — protect and age the lake: versioning, encryption, lifecycle."""
from lake_config import BUCKET, s3_client

s3 = s3_client()
s3.put_bucket_versioning(Bucket=BUCKET,
                         VersioningConfiguration={'Status': 'Enabled'})
s3.put_bucket_encryption(Bucket=BUCKET, ServerSideEncryptionConfiguration={
    'Rules': [{'ApplyServerSideEncryptionByDefault': {'SSEAlgorithm': 'AES256'}}]})
s3.put_bucket_lifecycle_configuration(Bucket=BUCKET, LifecycleConfiguration={
    'Rules': [{'ID': 'age-raw-zone', 'Status': 'Enabled',
               'Filter': {'Prefix': 'raw/'},
               'Transitions': [{'Days': 30, 'StorageClass': 'STANDARD_IA'},
                               {'Days': 180, 'StorageClass': 'GLACIER'}]}]})

print('Versioning:', s3.get_bucket_versioning(Bucket=BUCKET)['Status'])
rule = s3.get_bucket_lifecycle_configuration(Bucket=BUCKET)['Rules'][0]
print('Lifecycle rule:', rule['ID'], '->',
      [(t['Days'], t['StorageClass']) for t in rule['Transitions']])
