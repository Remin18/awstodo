import os
import http
import json
import boto3
from decimal import Decimal
from boto3.dynamodb.conditions import Attr
from urllib.parse import unquote

dynamodb = boto3.resource('dynamodb')
todo_table = dynamodb.Table(os.environ['TODO_TABLE'])

class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return int(obj)
        return json.JSONEncoder.default(self, obj)

def search_handler(event, context):

    userId = event["requestContext"]["authorizer"]["claims"]["sub"]
    search_word = event['pathParameters']['word']
    decoded_word = unquote(search_word)

    res = todo_table.scan(
        FilterExpression = (
            Attr('detail').contains(decoded_word) |
            Attr('title').contains(decoded_word)
        ) & Attr('userId').contains(userId)
    )

    return {
        "statusCode": http.HTTPStatus.OK,
        "body": json.dumps({
            "todos": res['Items']
        }, cls=JSONEncoder),
    }
