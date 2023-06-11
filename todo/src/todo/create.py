import json
import os
import uuid
import http
import boto3
from common import JSONEncoder

dynamodb = boto3.resource('dynamodb')
todo_table = dynamodb.Table(os.environ['TODO_TABLE'])

def create_handler(event, context):

    data = json.loads(event['body'])
    userId = event["requestContext"]["authorizer"]["claims"]["sub"]

    todo = {
        "id": str(uuid.uuid4()),
        "userId": userId,
        "title": data["title"],
        "detail": data["detail"],
        "status": 0,
    }

    todo_table.put_item(Item=todo)

    return {
        "statusCode": http.HTTPStatus.CREATED,
        "body": json.dumps(todo, cls=JSONEncoder)
    }
