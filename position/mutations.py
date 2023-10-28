import uuid
import boto3
from boto3.dynamodb.conditions import Key, Attr
import strawberry
from .type import Position

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("position")


@strawberry.type
class Mutation:
    @strawberry.field
    def add_position(
        self,
        open_date: str,
        close_date: str,
        price: float,
        volume: float,
        is_leveraged: bool,
        order_type: str,
        direction: str,
        description: str,
    ) -> Position:
        id = str(uuid.uuid1())
        data = {
            "id": id,
            "open_date": open_date,
            "close_date": close_date,
            "price": price,
            "volume": volume,
            "is_leveraged": is_leveraged,
            "order_type": order_type,
            "direction": direction,
            "description": description,
        }
        new_position = Position.from_row(data)
        table.put_item(Item=data)
        return new_position

    @strawberry.field
    def delete_position(self, id: str) -> Position:
        position = table.query(KeyConditionExpression=Key("id").eq(id))["Items"]
        if not position:
            raise Exception("position not found")
        table.delete_item(
            Key={"id": id},
        )
        position = position[0]
        return Position.from_row(position)

    @strawberry.field
    def update_position(
        self,
        id: str,
        open_date: str,
        close_date: str,
        price: float,
        volume: float,
        is_leveraged: bool,
        order_type: str,
        direction: str,
        description: str,
    ) -> Position:
        to_update = {}
        if open_date:
            to_update[":open_date"] = open_date
        if close_date:
            to_update[":close_date"] = close_date
        if price:
            to_update[":price"] = price
        if volume:
            to_update[":volume"] = volume
        if is_leveraged:
            to_update[":is_leveraged"] = is_leveraged
        if order_type:
            to_update[":order_type"] = order_type
        if direction:
            to_update[":direction"] = direction
        if description:
            to_update[":description"] = description
        response = None
        try:
            response = table.update_item(
                Key={"id": id},
                UpdateExpression="SET open_date = :open_date, close_date = :close_date, price = :price, volume = :volume, is_leveraged = :is_leveraged, order_type = :order_type, direction = :direction, description = :description",
                ExpressionAttributeValues=to_update,
                ReturnValues="UPDATED_NEW",
                ConditionExpression="attribute_exists(id)",
                ExpressionAttributeNames={},
            )
        except Exception as e:
            if "ConditionalCheckFailedException" in str(e):
                raise Exception("Position does not exist")
        return Position.from_row(
            {
                "id": id,
                "open_date": response["Attributes"]["open_date"],
                "close_date": response["Attributes"]["close_date"],
                "price": response["Attributes"]["price"],
                "volume": response["Attributes"]["volume"],
                "is_leveraged": response["Attributes"]["is_leveraged"],
                "order_type": response["Attributes"]["order_type"],
                "direction": response["Attributes"]["direction"],
                "description": response["Attributes"]["description"],
            }
        )
