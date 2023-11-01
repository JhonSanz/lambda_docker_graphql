import uuid
from decimal import Decimal
import boto3
from boto3.dynamodb.conditions import Key, Attr
import strawberry
from type import Deposit

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("deposit")


@strawberry.type
class Mutation:
    @strawberry.field
    def add_deposit(
        self,
        quantity: float,
        date_deposit: str,
        account_id: str,
        money_id: str,
        currency: str,
        description: str,
    ) -> Deposit:
        id = str(uuid.uuid1())
        data = {
            "id": id,
            "quantity": Decimal(quantity),
            "date_deposit": date_deposit,
            "account_id": account_id,
            "money_id": money_id,
            "currency": currency,
            "description": description,
        }
        new_deposit = Deposit.from_row(data)
        table.put_item(Item=data)
        return new_deposit

    @strawberry.field
    def delete_deposit(self, id: str) -> Deposit:
        deposit = table.query(KeyConditionExpression=Key("id").eq(id))["Items"]
        if not deposit:
            raise Exception("deposit not found")
        table.delete_item(
            Key={"id": id},
        )
        deposit = deposit[0]
        return Deposit.from_row(deposit)

    @strawberry.field
    def update_deposit(
        self,
        id: str,
        quantity: float,
        date_deposit: str,
        account_id: str,
        money_id: str,
        currency: str,
        description: str,
    ) -> Deposit:
        to_update = {}
        to_update[":quantity"] = quantity
        to_update[":date_deposit"] = date_deposit
        to_update[":account_id"] = account_id
        to_update[":money_id"] = money_id
        to_update[":currency"] = currency
        to_update[":description"] = description
        response = None
        try:
            response = table.update_item(
                Key={'id': id},
                UpdateExpression='SET quantity = :quantity, date_deposit = :date_deposit, account_id = :account_id, money_id = :money_id, currency = :currency, description = :description',
                ExpressionAttributeValues=to_update,
                ReturnValues='UPDATED_NEW',
                ConditionExpression='attribute_exists(id)',
            )
        except Exception as e:
            if "ConditionalCheckFailedException" in str(e):
                raise Exception("Deposit does not exist")
            raise Exception(str(e))
        return Deposit.from_row(
            {
                "id": id,
                "quantity": response["Attributes"]["quantity"],
                "date_deposit": response["Attributes"]["date_deposit"],
                "account_id": response["Attributes"]["account_id"],
                "money_id": response["Attributes"]["money_id"],
                "currency": response["Attributes"]["currency"],
                "description": response["Attributes"]["description"],
            }
        )
