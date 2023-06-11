import json
import os
import boto3
from decimal import Decimal
from boto3.dynamodb.conditions import Key
dynamodb = boto3.resource('dynamodb')
todo_table = dynamodb.Table(os.environ['TODO_TABLE'])

class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return int(obj)
        return json.JSONEncoder.default(self, obj)

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
