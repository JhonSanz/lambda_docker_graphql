import uuid
import boto3
from boto3.dynamodb.conditions import Key, Attr
import strawberry
from type import Deposit

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('deposit')

@strawberry.type
class Mutation:
	@strawberry.field
	def add_deposit(self, quantity: float, date_deposit: str, description: str) -> Deposit:
		id = str(uuid.uuid1())
		data = {
			'id': id,
			'quantity': quantity,
			'date_deposit': date_deposit,
			'description': description
		}
		new_deposit = Deposit.from_row(data)
		table.put_item(Item=data)
		return new_deposit

	@strawberry.field
	def delete_deposit(self, id: str) -> Deposit:
		deposit = table.query(
			KeyConditionExpression=Key('id').eq(id)
		)['Items']
		if not deposit:
			raise Exception('deposit not found')
		table.delete_item(
			Key={'id': id},
		)
		deposit = deposit[0]
		return Deposit.from_row(deposit)

	@strawberry.field
	def update_deposit(self, id: str, quantity: float, date_deposit: str, description: str) -> Deposit:
		to_update = {}
		if quantity: to_update[':quantity'] = quantity
		if date_deposit: to_update[':date_deposit'] = date_deposit
		if description: to_update[':description'] = description
		response = None
		try:
			response = table.update_item(
				Key={'id': id},
				UpdateExpression='SET quantity = :quantity, date_deposit = :date_deposit, description = :description',
				ExpressionAttributeValues=to_update,
				ReturnValues='UPDATED_NEW',
				ConditionExpression='attribute_exists(id)',
				ExpressionAttributeNames={}
			)
		except Exception as e:
			if 'ConditionalCheckFailedException' in str(e):
				raise Exception('Deposit does not exist')
		return Deposit.from_row({
			'id': id,
			'quantity': response['Attributes']['quantity'],
			'date_deposit': response['Attributes']['date_deposit'],
			'description': response['Attributes']['description']
		})