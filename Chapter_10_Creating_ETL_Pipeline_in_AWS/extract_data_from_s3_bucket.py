import boto3
import pandas as pd
# Step 1: Establish the boto3 s3 Client
s3 = boto3.client('s3')
bucket_name = 'my-new-aws-bucket-s3'
# Step 2: Define file path within "my-bucket-name" s3 bucket
crashes_key = 'traffic/traffic_crashes.csv'
# repeat for vehicles_key and people_key
# Step 3: Use s3.get_object() to reference the file "object" in the s3 bucket
crashes_response = s3.get_object(Bucket=bucket_name, Key=crashes_key)
## repeat for vehicles_response and people_response
# Step 4: Read in Data
crashes_df = pd.read_csv(crashes_response['Body'])
print(crashes_df)
## repeat for vehicles_df and people_df

