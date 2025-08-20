#download successful
import os
import sys
import boto3
from botocore.exceptions import ClientError
import logging

# Add parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# from config import CONFIG  
from config import CONFIG

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AWSJsonDownloader:
    """Class to handle downloading JSON files from AWS S3 using config from config.py."""
    
    def __init__(self):
        """Initialize with configuration loaded from config.py."""
        self.aws_access_key = CONFIG['aws_access_key_id']
        self.aws_secret_key = CONFIG['aws_secret_access_key']  
        self.aws_region = CONFIG['aws_region']
        self.metadata_bucket_name = CONFIG['metadata_bucket_name']
        self.schema_bucket_name = CONFIG['schema_bucket_name']
        self.metadata_key = CONFIG['metadata_file_key']
        self.schema_key = CONFIG['schema_file_key']
        self.download_path = CONFIG['download_path']
        self.s3_client = self.initialize_s3_client()
        
    def initialize_s3_client(self):
        """Initialize and return S3 client."""
        try:
            return boto3.client(
                's3',
                aws_access_key_id=self.aws_access_key,
                aws_secret_access_key=self.aws_secret_key,  
                region_name=self.aws_region
            )
        except Exception as e:
            logger.error(f"Error initializing S3 client: {str(e)}")
            raise
    
    def ensure_download_directory(self):
        """Create download directory if it doesn't exist."""
        try:
            os.makedirs(self.download_path, exist_ok=True)
        except Exception as e:
            logger.error(f"Error creating download directory: {str(e)}")
            raise
    
    def download_file(self, bucket_name, file_key, output_filename):
        """Download a single file from S3 to specified path."""
        try:
            output_path = os.path.join(self.download_path, output_filename)
            self.s3_client.download_file(
                bucket_name,
                file_key,
                output_path
            )
            logger.info(f"Successfully downloaded {file_key} from {bucket_name} to {output_path}")
            return output_path
        except ClientError as e:
            logger.error(f"Error downloading {file_key} from {bucket_name}: {str(e)}")
            raise
    
    def download_json_files(self):
        """Download both metadata and schema JSON files from different buckets."""
        try:
            self.ensure_download_directory()
            
            # Download metadata file
            metadata_filename = os.path.basename(self.metadata_key)
            metadata_path = self.download_file(self.metadata_bucket_name, self.metadata_key, metadata_filename)
            
            # # Download schema file
            schema_filename = os.path.basename(self.schema_key)
            schema_path = self.download_file(self.schema_bucket_name, self.schema_key, schema_filename)
            
            return {
                'metadata_path': metadata_path,
                'schema_path': schema_path
            }
        except Exception as e:
            logger.error(f"Error downloading JSON files: {str(e)}")
            raise

def main():
    """Main function to demonstrate usage."""
    try:
        downloader = AWSJsonDownloader()
        result = downloader.download_json_files()
        logger.info(f"Download completed. Files saved at: {result}")
    except Exception as e:
        logger.error(f"Failed to download files: {str(e)}")
        raise

if __name__ == "__main__":
    main()
#---------------------------------------------

# #download successful and refactoring both the json successful
# import os
# import sys
# import boto3
# import json
# from botocore.exceptions import ClientError
# import logging

# # Add parent directory to sys.path
# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# from config import CONFIG  # Import after adjusting path

# # Set up logging
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# class AWSJsonDownloader:
#     """Class to handle downloading JSON files from AWS S3 using config from config.py."""
    
#     def __init__(self):
#         """Initialize with configuration loaded from config.py."""
#         self.aws_access_key = CONFIG['aws_access_key_id']
#         self.aws_secret_access_key = CONFIG['aws_secret_access_key']
#         self.aws_region = CONFIG['aws_region']
#         self.metadata_bucket_name = CONFIG['metadata_bucket_name']
#         self.schema_bucket_name = CONFIG['schema_bucket_name']
#         self.metadata_key = CONFIG['metadata_file_key']
#         self.schema_key = CONFIG['schema_file_key']
#         self.download_path = CONFIG['download_path']
#         self.s3_client = self.initialize_s3_client()
        
#     def initialize_s3_client(self):
#         """Initialize and return S3 client."""
#         try:
#             return boto3.client(
#                 's3',
#                 aws_access_key_id=self.aws_access_key,
#                 aws_secret_access_key=self.aws_secret_access_key,
#                 region_name=self.aws_region
#             )
#         except Exception as e:
#             logger.error(f"Error initializing S3 client: {str(e)}")
#             raise
    
#     def ensure_download_directory(self):
#         """Create download directory if it doesn't exist."""
#         try:
#             os.makedirs(self.download_path, exist_ok=True)
#         except Exception as e:
#             logger.error(f"Error creating download directory: {str(e)}")
#             raise
    
#     def reformat_json_data(self, raw_data):
#         """Reformat the raw schema JSON data into a structured format."""
#         try:
#             formatted_data = {
#                 "name": raw_data["name"]["name"],
#                 "dataCatalogName": raw_data["name"]["dataCatalogName"],
#                 "datasets": []
#             }
            
#             for dataset in raw_data["dataSets"]:
#                 dataset_info = {
#                     "name": dataset["name"]["name"],
#                     "dataCatalogName": dataset["name"]["dataCatalogName"],
#                     "properties": [
#                         {
#                             "name": prop["name"]["name"],
#                             "dataCatalogName": prop["name"]["dataCatalogName"],
#                             "type": prop["type"],
#                             "nullable": prop["nullable"],
#                             "primaryKey": prop["primaryKey"],
#                             "uniqueKey": prop["uniqueKey"],
#                             "compositeKey": prop.get("compositeKey", False),
#                             "compositeKeyColumns": prop.get("compositeKeyColumns", [])
#                         }
#                         for prop in dataset["properties"]
#                     ],
#                     "relationships": [
#                         {
#                             "relationshipName": rel["relationshipName"]["name"],
#                             "dataCatalogName": rel["relationshipName"]["dataCatalogName"],
#                             "sourceDataset": rel["sourceDataset"]["name"],
#                             "sourceDataCatalogName": rel["sourceDataset"]["dataCatalogName"],
#                             "targetDataset": rel["targetDataset"]["name"],
#                             "targetDataCatalogName": rel["targetDataset"]["dataCatalogName"],
#                             "sourceFields": [field["name"] for field in rel["sourceFields"]],
#                             "targetFields": [field["name"] for field in rel["targetFields"]]
#                         }
#                         for rel in dataset.get("dataSetRelationShips", [])
#                     ]
#                 }
#                 formatted_data["datasets"].append(dataset_info)
            
#             return formatted_data
#         except Exception as e:
#             logger.error(f"Error reformatting schema JSON data: {str(e)}")
#             raise
    
#     def reformat_metadata_json_data(self, raw_data):
#         """Reformat the raw metadata JSON data into a structured format."""
#         try:
#             formatted_data = {
#                 "nodes": [],
#                 "links": [],
#                 "prefix": raw_data.get("prefix", ""),
#             }
            
#             # Process nodes
#             for node in raw_data.get("nodes", []):
#                 node_info = {
#                     "id": node["id"],
#                     "node_type": node["node_type"],
#                     "label": node["label"],
#                     "data_type": node.get("data_type"),
#                     "nullable": node.get("nullable"),
#                     "primary_key": node.get("primary_key"),
#                     "unique_key": node.get("unique_key"),
#                     "foreign_key": node.get("foreign_key"),
#                     "composite_key": node.get("composite_key"),
#                     "composite_key_columns": node.get("composite_key_columns", []),
#                     "uri": node.get("uri"),
#                     "identity": node.get("identity"),
#                     "dataSourceID": node.get("dataSourceID")
#                 }
#                 formatted_data["nodes"].append(node_info)
            
#             # Process links
#             for link in raw_data.get("links", []):
#                 link_info = {
#                     "source": link["source"],
#                     "target": link["target"],
#                     "relationship": link["relationship"],
#                     "node_uri": link.get("node_uri"),
#                     "rel_uri": link.get("rel_uri"),
#                     "prefLabel": link.get("prefLabel"),
#                     "altLabel": link.get("altLabel"),
#                     "primaryKey": link.get("primaryKey"),
#                     "uniqueKey": link.get("uniqueKey"),
#                     "identity": link.get("identity"),
#                     "target_node_uri": link.get("target_node_uri"),
#                     "pathIds": link.get("pathIds", []),
#                     "metrics": link.get("metrics", {}),
#                     "target_column": link.get("target_column"),
#                     "dashed": link.get("dashed")
#                 }
#                 formatted_data["links"].append(link_info)
            
#             return formatted_data
#         except Exception as e:
#             logger.error(f"Error reformatting metadata JSON data: {str(e)}")
#             raise
    
#     def download_file(self, bucket_name, file_key, output_filename):
#         """Download a single file from S3 and reformat before saving."""
#         try:
#             # Download the file content
#             response = self.s3_client.get_object(Bucket=bucket_name, Key=file_key)
#             raw_data = json.loads(response['Body'].read().decode('utf-8'))
            
#             # Reformat the JSON data based on file key
#             if file_key == self.metadata_key:
#                 formatted_data = self.reformat_json_data(raw_data)  # For schema structure
#             elif file_key == self.schema_key:
#                 formatted_data = self.reformat_metadata_json_data(raw_data)  # For metadata structure
#             else:
#                 formatted_data = raw_data  # Fallback for unrecognized files
            
#             # Save the reformatted data to the specified path
#             output_path = os.path.join(self.download_path, output_filename)
#             with open(output_path, 'w') as f:
#                 json.dump(formatted_data, f, indent=4)
#             logger.info(f"Successfully downloaded and reformatted {file_key} from {bucket_name} to {output_path}")
#             return output_path
#         except ClientError as e:
#             logger.error(f"Error downloading {file_key} from {bucket_name}: {str(e)}")
#             raise
#         except Exception as e:
#             logger.error(f"Error processing {file_key}: {str(e)}")
#             raise
    
#     def download_json_files(self):
#         """Download both metadata and schema JSON files from different buckets."""
#         try:
#             self.ensure_download_directory()
            
#             # Download metadata file
#             metadata_filename = os.path.basename(self.metadata_key)
#             metadata_path = self.download_file(self.metadata_bucket_name, self.metadata_key, metadata_filename)
            
#             # Download schema file
#             schema_filename = os.path.basename(self.schema_key)
#             schema_path = self.download_file(self.schema_bucket_name, self.schema_key, schema_filename)
            
#             return {
#                 'metadata_path': metadata_path,
#                 'schema_path': schema_path
#             }
#         except Exception as e:
#             logger.error(f"Error downloading JSON files: {str(e)}")
#             raise

# def main():
#     """Main function to demonstrate usage."""
#     try:
#         downloader = AWSJsonDownloader()
#         result = downloader.download_json_files()
#         logger.info(f"Download completed. Files saved at: {result}")
#     except Exception as e:
#         logger.error(f"Failed to download files: {str(e)}")
#         raise

# if __name__ == "__main__":
#     main()
