import boto3
def lambda_handler(event, context):
    s3 = boto3.client('s3')
    bucket_name =event["bucket_name"]
    crashes_key = event["crashes_key"]
    # repeat for vehicles_key and people_key
    crashes_response = s3.get_object(Bucket=bucket_name,Key=crashes_key)
    ## repeat for vehicles_response and people_response
    return {"crashes_response": crashes_response}