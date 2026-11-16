"""Chapter 9, Step 5 — versioning and lifecycle rules on the bucket."""
import sys

from lake_config import BUCKET, MODE, gcs_client

if MODE != 'gcp':
    sys.exit('The emulator does not support bucket settings. '
             'Run this step on Google Cloud (Step 4).')

bucket = gcs_client().get_bucket(BUCKET)
bucket.versioning_enabled = True
bucket.add_lifecycle_set_storage_class_rule('NEARLINE', age=30, matches_prefix=['raw/'])
bucket.add_lifecycle_set_storage_class_rule('ARCHIVE', age=180, matches_prefix=['raw/'])
bucket.patch()

bucket.reload()
print('Versioning:', bucket.versioning_enabled)
for rule in bucket.lifecycle_rules:
    print('Rule:', rule['action'], rule['condition'])
