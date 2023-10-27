import json
import boto3
import strawberry
from gql_strawberry.query import Query
from gql_strawberry.mutations import Mutation


def handler(event, context):
    body = json.loads(event["body"])
    if not body.get("query"):
        return {
            'statusCode': 400,
            'body': "Bad body bro"
        }

    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table("broker")

    schema = strawberry.Schema(query=Query, mutation=Mutation(table=table))
    result = schema.execute_sync(body['query'])
    return {
        'statusCode': 200,
        'body': json.dumps(
            {
                "data": result.data,
                "errors": [
                    {
                        "msg": err.message,
                        "location": [
                            {"line": loc.line, "column": loc.column}
                            for loc in err.locations
                        ]
                    }
                    for err in result.errors
                ] if result.errors else []
            }
        )
    }
