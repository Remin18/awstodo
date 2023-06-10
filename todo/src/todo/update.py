import os
import http
import json

import boto3
dynamodb = boto3.resource('dynamodb')
todo_table = dynamodb.Table(os.environ['TODO_TABLE'])

def update_handler(event, context):

    data = json.loads(event['body'])
    todo_id = event['pathParameters']['todo_id']

    todo = todo_table.update_item(
        Key={'id': todo_id},
        UpdateExpression="set title = :t, detail = :d, #s = :s",
        ExpressionAttributeNames={
            '#s': 'status' # DynamoDBの予約語のためマッピング
        },
        ExpressionAttributeValues={
            ':t': data["title"],
            ':d': data["detail"],
            ':s': data["status"]
        },
        ReturnValues="UPDATED_NEW"
    )

    return {
        "statusCode": http.HTTPStatus.NO_CONTENT,
        "body": json.dumps(todo)
    }
