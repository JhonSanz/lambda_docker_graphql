import typing
import strawberry
import boto3
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource("dynamodb")


@strawberry.type
class Money:
    id: str
    currency: str
