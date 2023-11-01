import uuid
from decimal import Decimal
import boto3
from boto3.dynamodb.conditions import Key, Attr
import strawberry
from type import Money

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("money")


@strawberry.type
class Mutation:
    @strawberry.field
    def add_money(self, currency: str) -> Money:
        id = str(uuid.uuid1())
        data = {"id": id, "currency": currency}
        new_money = Money.from_row(data)
        table.put_item(Item=data)
        return new_money

    @strawberry.field
    def delete_money(self, id: str) -> Money:
        money = table.query(KeyConditionExpression=Key("id").eq(id))["Items"]
        if not money:
            raise Exception("money not found")
        table.delete_item(
            Key={"id": id},
        )
        money = money[0]
        return Money.from_row(money)

    @strawberry.field
    def update_money(self, id: str, currency: str) -> Money:
        to_update = {}
        to_update[":currency"] = currency
        response = None
        try:
            response = table.update_item(
                Key={'id': id},
                UpdateExpression='SET currency = :currency',
                ExpressionAttributeValues=to_update,
                ReturnValues='UPDATED_NEW',
                ConditionExpression='attribute_exists(id)',
            )
        except Exception as e:
            if "ConditionalCheckFailedException" in str(e):
                raise Exception("Money does not exist")
            raise Exception(str(e))
        return Money.from_row(
            {"id": id, "currency": response["Attributes"]["currency"]}
        )
