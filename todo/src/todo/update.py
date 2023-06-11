import os
import http
import json
import boto3
from common import UserInfo, JSONEncoder

dynamodb = boto3.resource('dynamodb')
todo_table = dynamodb.Table(os.environ['TODO_TABLE'])

ADD_EXP = 5

def update_handler(event, context):

    data = json.loads(event['body'])
    todo_id = event['pathParameters']['todo_id']
    userId = event["requestContext"]["authorizer"]["claims"]["sub"]

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

    # 完了済みの場合に経験値を加算
    if data["status"] == 1:
        user_info = UserInfo(userId)
        user_info.add_exp(ADD_EXP)

    return {
        "statusCode": http.HTTPStatus.NO_CONTENT,
        "body": json.dumps(todo, cls=JSONEncoder)
    }
