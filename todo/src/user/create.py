import boto3
import os
import http
import json

client_id = os.environ['CLIENT_ID']
region = os.environ['REGION']
client = boto3.client('cognito-idp', region_name=region)

def create_user_handler(event, context):

    body = json.loads(event['body'])
    username = body['username']
    password = body['password']

    response = client.sign_up(
        ClientId=client_id,
        Username=username,
        Password=password
    )

    return {
        'statusCode':http.HTTPStatus.OK
    }
