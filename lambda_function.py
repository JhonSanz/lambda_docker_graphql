import json
import strawberry
from gql_strawberry.query import Query
from gql_strawberry.mutations import Mutation


def handler(event, context):
    body = json.loads(event["body"])
    if not body.get("query"):
        return {
            'statusCode': 400,
            'body': {
                "msg": "Bad body bro"
            }
        }

    schema = strawberry.Schema(query=Query, mutation=Mutation)
    result = schema.execute_sync(body['query'])
    return {
        'statusCode': 200,
        'body': {
            "msg": result.__dict__
        }
    }
