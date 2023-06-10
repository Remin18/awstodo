import json
import os
import uuid
import http

import boto3
dynamodb = boto3.resource('dynamodb')
todo_table = dynamodb.Table(os.environ['TODO_TABLE'])

def create_handler(event, context):

    data = json.loads(event['body'])

    todo = {
        "id": str(uuid.uuid4()),
        "deadline_date": "",
        "detail": "",
        "status": "new",
        "title": data["title"]
    }

    todo_table.put_item(Item=todo)

    return {
        "statusCode": http.HTTPStatus.CREATED,
        "body": json.dumps(todo),
    }