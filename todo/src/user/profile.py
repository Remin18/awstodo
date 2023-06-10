import os
import http
import json
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
user_table = dynamodb.Table(os.environ['USER_TABLE'])

def profile_handler(event, context):

    userId = event["requestContext"]["authorizer"]["claims"]["sub"]

    res = user_table.query(
        KeyConditionExpression=Key('user_id').eq(userId),
    )

    user_data = res['Items'][0]
    data = {
        'user_id': user_data['user_id'],
        'name': user_data['name'],
        'level': str(user_data['level']),
        'exp': str(user_data['exp']),
    }

    return {
        "statusCode": http.HTTPStatus.OK,
        "body": json.dumps({
            "user": data
        }),
    }
