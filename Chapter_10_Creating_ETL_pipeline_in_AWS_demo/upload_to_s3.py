import boto3
# Step 1: Establish the boto3 s3 Client
s3 = boto3.client('s3')
bucket_name = 'my-new-aws-bucket-s3'
# Step 2: Define file paths within your local environment
crashes_path = '/home/ankit/Desktop/ml/ETL/Building_ETL_Pipelines_with_Python/Building-ETL-Pipelines-with-Python/Chapters/chapter_10/data/traffic_crashes.csv'
# repeat for vehicles_path and people_path
# Step 3: Define output file paths within "my-bucket-name" s3 bucket in a 'traffic' directory
crashes_key = 'traffic/traffic_crashes.csv'
# repeat for vehicles_key and people_key
# upload the file
s3. upload_file(Filename=crashes_path, Bucket=bucket_name, Key=crashes_key)
# repeat for vehicles and people