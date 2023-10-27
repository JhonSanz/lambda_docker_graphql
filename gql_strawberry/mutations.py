import uuid
import boto3
from boto3.dynamodb.conditions import Key, Attr
import strawberry
from .type import Broker


dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table("broker")

@strawberry.type
class Mutation:
    @strawberry.field
    def add_broker(self, name: str, website: str) -> Broker:
        """
            mutation {
                addBroker(name: "xm", website: "https://xm.com") {
                    id
                    name
                    website
                }
            }
        """
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
        """
            mutation {
                deleteBroker(id: "73aad074-7441-11ee-a952-d89c679e8b2c") {
                    id
                    name
                    website
                }
            }
        """
        broker = table.query(
            KeyConditionExpression=Key('id').eq(id)
        )["Items"]
        if not broker:
            raise Exception("broker not found")
        table.delete_item(
            Key={"id": id},
        )
        broker = broker[0]
        return Broker.from_row(broker)

    @strawberry.field
    def update_broker(id: str, name: str = "", website: str = "") -> Broker:
        """
            mutation {
                updateBroker(
                    id: "73aad073214-7441-11ee-a952-d89c679e8b2c",
                    name: "xxxm",
                    website: "https://xm.com"
                ) {
                    id
                    name
                    website
                }
            }
        """
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