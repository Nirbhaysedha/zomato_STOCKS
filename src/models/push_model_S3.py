# this code is used to send the model to s3 bucket!
# boto3 is used to push data on s3 bucket
import boto3 # boto3 is sdk
import shutil
from botocore.exceptions import NoCredentialsError

def upload_to_s3(local_file_path, bucket_name, s3_file_path):
    s3 = boto3.client('s3')

    try:
        # Upload the file
        s3.upload_file(local_file_path, bucket_name, s3_file_path)
        print(f"File uploaded successfully to {bucket_name}/{s3_file_path}")
    except FileNotFoundError:
        print(f"The file {local_file_path} was not found.")
    except NoCredentialsError:
        print("Credentials not available.")

# Example usage
local_model_path = 'models/model.joblib'
s3_bucket_name = 'nyc-projecr'
s3_file_path = 'models/model.joblib' 

upload_to_s3(local_model_path, s3_bucket_name, s3_file_path)
shutil.copy(local_model_path, 'model.joblib')
