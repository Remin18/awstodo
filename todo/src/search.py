import os
import http
import json

import boto3
from boto3.dynamodb.conditions import Attr
from urllib.parse import unquote

dynamodb = boto3.resource('dynamodb')
todo_table = dynamodb.Table(os.environ['TODO_TABLE'])

def search_handler(event, context):

    search_word = event['pathParameters']['word']
    decoded_word = unquote(search_word)

    res = todo_table.scan(
        FilterExpression = Attr('detail').contains(decoded_word) |
                           Attr('title').contains(decoded_word),
    )

    return {
        "statusCode": http.HTTPStatus.OK,
        "body": json.dumps({
            "todos": res['Items']
        }),
    }
