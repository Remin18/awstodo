import json
import boto3
import os
import http

client_id = os.environ['CLIENT_ID']
region = os.environ['REGION']
client = boto3.client('cognito-idp', region_name=region)

def auth_handler(event, context):

    body = json.loads(event['body'])
    username = body['username']
    password = body['password']

    try:
        response = client.initiate_auth(
            AuthFlow='USER_PASSWORD_AUTH',
            AuthParameters={
                'USERNAME': username,
                'PASSWORD': password
            },
            ClientId=client_id
        )

        id_token = response['AuthenticationResult']['IdToken']

        return {
            'statusCode': http.HTTPStatus.OK,
            'body': id_token
        }
    except Exception as e:
        print(str(e))
        return {
            'statusCode': http.HTTPStatus.INTERNAL_SERVER_ERROR,
            'body': 'An error occurred while initiating authentication'
        }
