import json
import boto3
import strawberry
from gql_strawberry.query import Query
from gql_strawberry.mutations import Mutation


# def handler(event, context):
#     body = json.loads(event["body"])
#     if not body.get("query"):
#         return {
#             'statusCode': 400,
#             'body': "Bad body bro"
#         }

#     dynamodb = boto3.resource('dynamodb')
#     table = dynamodb.Table("broker")

#     schema = strawberry.Schema(query=Query, mutation=Mutation(table=table))
#     result = schema.execute_sync(body['query'])
#     return {
#         'statusCode': 200,
#         'body': json.dumps(
#             {
#                 "data": result.data,
#                 "errors": [
#                     {
#                         "msg": err.message,
#                         "location": [
#                             {"line": loc.line, "column": loc.column}
#                             for loc in err.locations
#                         ]
#                     }
#                     for err in result.errors
#                 ] if result.errors else []
#             }
#         )
#     }


import boto3
import uuid
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table("broker")

schema = strawberry.Schema(query=Query, mutation=Mutation)
# result = schema.execute_sync(
#     """
#         mutation {
#             addBroker(name: "xm", website: "https://xm.com") {
#                 id
#                 name
#                 website
#             }
#         }
#     """
# )

# result = schema.execute_sync(
#     """
#         query {
#             broker(id: "73aad074-7441-11ee-a952-d89c679e8b2c") {
#                 id
#                 website
#             }
#         }
#     """
# )

# result = schema.execute_sync(
#     """
#         query {
#             broker(id: "73aad074-7441-11ee-a952-d89c679e8b2c") {
#                 id
#                 website
#                 other {
#                     msg
#                 }
#             }
#         }
#     """
# )

# result = schema.execute_sync(
#     """
#         mutation {
#             updateBroker(id: "73aad073214-7441-11ee-a952-d89c679e8b2c", name: "xxxm", website: "https://xm.com") {
#                 id
#                 name
#                 website
#             }
#         }
#     """
# )


# result = schema.execute_sync(
#     """
#         mutation {
#             deleteBroker(id: "73aad074-7441-11ee-a952-d89c679e8b2c") {
#                 id
#                 name
#                 website
#             }
#         }
#     """
# )

result = schema.execute_sync(
    """
        {
        brokers(orderBy: "id", offset: 0, limit: 4) {
            items {
            website
            }
            totalItemsCount
        }
        }
    """
)

print(result)

