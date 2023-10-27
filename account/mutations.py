import uuid
import boto3
from boto3.dynamodb.conditions import Key, Attr
import strawberry
from .type import Account

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('account')

@strawberry.type
class Mutation:
	@strawberry.field
	def add_account(self, name: str, details: str, leverage: float, account_type: str) -> Account:
		id = str(uuid.uuid1())
		new_account = Account.from_row({ 
				'id': id,
				'name': name,
				'details': details,
				'leverage': leverage,
				'account_type': account_type
		})
		table.put_item(
			Item={
				'id': id,
				'name': name,
				'details': details,
				'leverage': leverage,
				'account_type': account_type
			}
		)
		return new_account

	@strawberry.field
	def delete_account(self, id: str) -> Account:
		account = table.query(
			KeyConditionExpression=Key('id').eq(id)
		)['Items']
		if not account:
			raise Exception('account not found')
		table.delete_item(
			Key={'id': id},
		)
		account = account[0]
		return Account.from_row(account)

	@strawberry.field
	def update_account(self, id: str, name: str, details: str, leverage: float, account_type: str) -> Account:
		to_update = {}
		if name: to_update[':name'] = name
		if details: to_update[':details'] = details
		if leverage: to_update[':leverage'] = leverage
		if account_type: to_update[':account_type'] = account_type
		response = None
		try:
			response = table.update_item(
				Key={'id': id},
				UpdateExpression='SET name = :name, details = :details, leverage = :leverage, account_type = :account_type',
				ExpressionAttributeValues=to_update,
				ReturnValues='UPDATED_NEW',
				ConditionExpression='attribute_exists(id)',
				ExpressionAttributeNames={}
			)
		except Exception as e:
			if 'ConditionalCheckFailedException' in str(e):
				raise Exception('Account does not exist')
		return Account.from_row({
			'id': id,
			'name': response['Attributes']['name'],
			'details': response['Attributes']['details'],
			'leverage': response['Attributes']['leverage'],
			'account_type': response['Attributes']['account_type']
		})