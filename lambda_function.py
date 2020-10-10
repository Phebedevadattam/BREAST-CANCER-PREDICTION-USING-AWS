import os
import io
import boto3
import json
import csv
def lambda_handler(event, context):
    ENDPOINT_NAME = os.environ['ENDPOINT_NAME']
    runtime= boto3.client('runtime.sagemaker')
    print(ENDPOINT_NAME)
    print("Received event: " , json.dumps(event, indent=2))
    data = json.loads(json.dumps(event))
    print("Data:",data)
    payload = data['data']
    print("Payload:",payload)
    response = runtime.invoke_endpoint(EndpointName=ENDPOINT_NAME,
                                       ContentType='text/csv',
                                       Body=payload)
    result = json.loads(response['Body'].read().decode())
    sns = boto3.client('sns')
    print(result)

    if result>0.5:
      response = sns.publish(TopicArn='arn:aws:sns:us-east-1:359016722223:cancer',Message='According to the data you have provided, the result is Bengin',Subject="Cancer Prediction",)
      return "Benign"
    else:
      response = sns.publish(TopicArn='arn:aws:sns:us-east-1:359016722223:cancer',Message='According to the data you have provided, the result is Malignant',Subject="Cancer Prediction",)
      return "Malignant"
