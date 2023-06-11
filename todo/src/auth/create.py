import boto3
import os
import http
import json

client_id = os.environ['CLIENT_ID']
client = boto3.client('cognito-idp')

def create_user_handler(event, context):

    body = json.loads(event['body'])
    username = body['username']
    password = body['password']

    try:
        response = client.sign_up(
            ClientId=client_id,
            Username=username,
            Password=password
        )

        return {
            'statusCode': http.HTTPStatus.OK,
            'body': 'user create successfully'
        }
    except Exception as e:
        print(str(e))
        return {
            'statusCode': http.HTTPStatus.INTERNAL_SERVER_ERROR,
            'body': 'An error occurred while creating user'
        }
