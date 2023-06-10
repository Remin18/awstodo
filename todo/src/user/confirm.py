import boto3
import os
import json
import http

client_id = os.environ['CLIENT_ID']
user_pool_id = os.environ['USERPOOL_ID']
region = os.environ['REGION']
client = boto3.client('cognito-idp', region_name=region)

def confirm_handler(event, context):

    body = json.loads(event['body'])
    username = body['username']
    password = body['password']

    try:
        response = client.admin_set_user_password(
            UserPoolId=user_pool_id,
            Username=username,
            Password=password,
            Permanent=True
        )

        return {
            'statusCode': http.HTTPStatus.OK,
            'body': 'Password changed successfully'
        }
    except Exception as e:
        print(str(e))
        return {
            'statusCode': http.HTTPStatus.INTERNAL_SERVER_ERROR,
            'body': 'An error occurred while changing the password'
        }
