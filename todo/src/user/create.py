import json
import os
import uuid
import http

import boto3
dynamodb = boto3.resource('dynamodb')
user_table = dynamodb.Table(os.environ['USER_TABLE'])

def create_handler(event, context):

    data = json.loads(event['body'])
    userId = event["requestContext"]["authorizer"]["claims"]["sub"]

    user = {
        "user_id": userId,
        "name": data["username"],
        "exp": 0,
        "level": 1,
    }

    user_table.put_item(Item=user)

    return {
        "statusCode": http.HTTPStatus.CREATED,
        "body": json.dumps({
            "user": user
        })
    }
