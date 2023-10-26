import uuid
import boto3
import strawberry
from .type import Broker
from .data import brokers


dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table("broker")

@strawberry.type
class Mutation:
    @strawberry.field
    def add_broker(self, name: str, website: str) -> Broker:
        id = str(uuid.uuid1())
        new_broker = Broker.from_row({
            "id": id,
            "name": name,
            "website": website
        })
        table.put_item(
            Item={
                'id': id,
                'name': name,
                'website': website,
            }
        )
        return new_broker

    @strawberry.field
    def delete_broker(self, id: str) -> Broker:
        to_delete = list(filter(lambda x: x["id"] == id, brokers))
        if not to_delete:
            raise Exception("Broker does not exist")
        to_delete = to_delete[0]
        brokers.remove(to_delete)
        return Broker.from_row({
            "id": to_delete["id"],
            "name": to_delete["name"],
            "website": to_delete["website"]
        })

    @strawberry.field
    def update_broker(id: str, name: str = "", website: str = "") -> Broker:
        to_update = {}
        if name: to_update[":name"] = name
        if website: to_update[":website"] = website
        response = None
        try:
            response = table.update_item(
                Key={'id': id},
                UpdateExpression="SET #broker_name = :name, website = :website",
                ExpressionAttributeValues=to_update,
                ReturnValues="UPDATED_NEW",
                ConditionExpression="attribute_exists(id)",
                ExpressionAttributeNames={
                    "#broker_name": "name"
                }
            )
        except Exception as e:
            if "ConditionalCheckFailedException" in str(e):
                raise Exception("Broker does not exist")
        
        return Broker.from_row({
            "id": id,
            "name": response["Attributes"]["name"],
            "website": response["Attributes"]["website"]
        })