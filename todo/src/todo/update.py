import os
import http
import json
import boto3
import bisect
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb')
todo_table = dynamodb.Table(os.environ['TODO_TABLE'])
user_table = dynamodb.Table(os.environ['USER_TABLE'])

ADD_EXP = 5

class UserInfo(object):

    EXP_LEVEL_DICT = {
        # total_exp : level
        0: 1,
        10: 2,
        20: 3,
        30: 4,
        40: 5,
        50: 6,
    }

    def __init__(self, user_id) -> None:
        self.user_id = user_id

    def add_exp(self, exp):
        user_data = self._get_user_data()
        new_exp = user_data['exp'] + exp
        level = self._get_level_by_exp(new_exp)

        user_table.update_item(
            Key={'user_id': self.user_id},
            UpdateExpression='SET exp = :e, #l = :l',
            ExpressionAttributeNames={
                '#l': 'level' # DynamoDBの予約語のためマッピング
            },
            ExpressionAttributeValues={
                ':e': new_exp,
                ':l': level
            }
        )

    def _get_level_by_exp(self, exp):
        exp_list = list(self.EXP_LEVEL_DICT.keys())
        idx = bisect.bisect(exp_list, exp) - 1
        return self.EXP_LEVEL_DICT[exp_list[idx]]

    def _get_user_data(self):
        res = user_table.query(
            KeyConditionExpression=Key('user_id').eq(self.user_id),
        )
        return res['Items'][0]

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
    if data["status"] == "1":
        user_info = UserInfo(userId)
        user_info.add_exp(ADD_EXP)

    return {
        "statusCode": http.HTTPStatus.NO_CONTENT,
        "body": json.dumps(todo)
    }
