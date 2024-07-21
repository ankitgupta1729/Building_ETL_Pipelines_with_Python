def lambda_handler(event, context):
    bucket_name = event["bucket_name"]
    crashes_key= 'traffic/traffic_crashes.csv'
    ## repeat for vehicles_key and people_key
    return{"bucket_name": bucket_name,"crashes_key":crashes_key}