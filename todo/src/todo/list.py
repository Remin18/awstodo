import json
import os
import boto3
from boto3.dynamodb.conditions import Key
from common import JSONEncoder

dynamodb = boto3.resource('dynamodb')
todo_table = dynamodb.Table(os.environ['TODO_TABLE'])

def list_handler(event, context):

    userId = event["requestContext"]["authorizer"]["claims"]["sub"]
    res = todo_table.scan(
        FilterExpression=Key('userId').eq(userId)
    )

    return {
        "statusCode": 200,
        "body": json.dumps({
            "todos": res['Items']
        }, cls=JSONEncoder),
    }
