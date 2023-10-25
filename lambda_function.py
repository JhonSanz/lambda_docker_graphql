
import strawberry
from gql_strawberry.query import Query
from gql_strawberry.mutations import Mutation


def handler(event, context):
    schema = strawberry.Schema(query=Query, mutation=Mutation)
    result = schema.execute_sync(event['query'])
    return {
        'statusCode': 200,
        'body': {
            "msg": result.__dict__
        }
    }
