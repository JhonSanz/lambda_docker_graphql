import uuid
from decimal import Decimal
import boto3
from boto3.dynamodb.conditions import Key, Attr
import strawberry
from type import Broker

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("broker")


@strawberry.type
class Mutation:
    @strawberry.field
    def add_broker(self, name: str, website: str) -> Broker:
        id = str(uuid.uuid1())
        data = {"id": id, "name": name, "website": website}
        new_broker = Broker.from_row(data)
        table.put_item(Item=data)
        return new_broker

    @strawberry.field
    def delete_broker(self, id: str) -> Broker:
        broker = table.query(KeyConditionExpression=Key("id").eq(id))["Items"]
        if not broker:
            raise Exception("broker not found")
        table.delete_item(
            Key={"id": id},
        )
        broker = broker[0]
        return Broker.from_row(broker)

    @strawberry.field
    def update_broker(self, id: str, name: str, website: str) -> Broker:
        to_update = {}
        if name:
            to_update[":name"] = name
        if website:
            to_update[":website"] = website
        response = None
        try:
            response = table.update_item(
                Key={"id": id},
                UpdateExpression="SET name = :name, website = :website",
                ExpressionAttributeValues=to_update,
                ReturnValues="UPDATED_NEW",
                ConditionExpression="attribute_exists(id)",
                ExpressionAttributeNames={},
            )
        except Exception as e:
            if "ConditionalCheckFailedException" in str(e):
                raise Exception("Broker does not exist")
        return Broker.from_row(
            {
                "id": id,
                "name": response["Attributes"]["name"],
                "website": response["Attributes"]["website"],
            }
        )
