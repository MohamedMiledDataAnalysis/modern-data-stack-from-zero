"""Chapter 9, Step 5 — versioning and lifecycle rules on the bucket."""
from lake_config import BUCKET, gcs_client

bucket = gcs_client().get_bucket(BUCKET)
bucket.versioning_enabled = True
bucket.add_lifecycle_set_storage_class_rule('NEARLINE', age=30, matches_prefix=['raw/'])
bucket.add_lifecycle_set_storage_class_rule('ARCHIVE', age=180, matches_prefix=['raw/'])
bucket.patch()

bucket.reload()
print('Versioning:', bucket.versioning_enabled)
for rule in bucket.lifecycle_rules:
    print('Rule:', rule['action'], rule['condition'])
