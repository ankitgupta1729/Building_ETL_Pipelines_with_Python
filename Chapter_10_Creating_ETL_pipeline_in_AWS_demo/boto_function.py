import boto3
def lambda_handler(event, context):
    s3 = boto3.client('s3')
    return {"s3": s3, "bucket_name": 'my-bucket-name'}