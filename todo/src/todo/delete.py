import os
import http

import boto3
dynamodb = boto3.resource('dynamodb')
todo_table = dynamodb.Table(os.environ['TODO_TABLE'])

def delete_handler(event, context):

    todo_id = event['pathParameters']['todo_id']
    todo_table.delete_item(Key={'id': todo_id})

    return {
        "statusCode": http.HTTPStatus.NO_CONTENT,
        "body": "",
    }
