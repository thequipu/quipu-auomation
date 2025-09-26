import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configuration dictionary for AWS and file paths
CONFIG = {
    'aws_access_key_id': os.getenv('AWS_ACCESS_KEY_ID'),
    'aws_secret_access_key': os.getenv('AWS_SECRET_ACCESS_KEY'),
    'aws_region': os.getenv('AWS_REGION'),
    'metadata_bucket_name': os.getenv('METADATA_BUCKET_NAME'),
    'schema_bucket_name': os.getenv('SCHEMA_BUCKET_NAME'),
    'metadata_file_key': os.getenv('METADATA_FILE_KEY'),
    'schema_file_key': os.getenv('SCHEMA_FILE_KEY'),
    'download_path': os.getenv('DOWNLOAD_PATH', '../downloads'),
    's3_bucket': os.getenv('S3_BUCKET'),
    's3_key': os.getenv('S3_KEY'),
}

# Validate required configuration
required_keys = [
    'AWS_ACCESS_KEY_ID', 
    'AWS_SECRET_ACCESS_KEY', 
    'AWS_REGION',
    'METADATA_BUCKET_NAME', 
    'SCHEMA_BUCKET_NAME', 
    'METADATA_FILE_KEY',
]
missing_keys = [key for key in required_keys if not os.getenv(key)]
if missing_keys:
    raise ValueError(f"Missing required environment variables: {missing_keys}")

# Verify that all CONFIG values are properly set
invalid_configs = [key for key, value in CONFIG.items() if value is None]
if invalid_configs:
    raise ValueError(f"Configuration values are None for keys: {invalid_configs}")