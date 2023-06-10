import json
import os

import boto3
dynamodb = boto3.resource('dynamodb')
todo_table = dynamodb.Table(os.environ['TODO_TABLE'])

def list_handler(event, context):

    res = todo_table.scan()

    return {
        "statusCode": 200,
        "body": json.dumps({
            "todos": res['Items']
        }),
    }
