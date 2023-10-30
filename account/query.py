import strawberry
import boto3
from boto3.dynamodb.conditions import Key
from type import Account
from utils import PaginationWindow, get_pagination_window


dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('account')

@strawberry.type
class Query:
	@strawberry.field(description='Get a list of account')
	def accounts(
		self,
		order_by: str,
		limit: int,
		offset: int = 0,
		name: str | None = None,
	) -> PaginationWindow[Account]:
		response = table.scan()
		accounts = response['Items']

		while 'LastEvaluatedKey' in response:
			response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
			accounts.extend(response['Items'])

		filters = {}
		if name:
			filters['name'] = name
		return get_pagination_window(
			dataset=accounts,
			ItemType=Account,
			order_by=order_by,
			limit=limit,
			offset=offset,
			filters=filters,
		)

	@strawberry.field(description='Get a account record.')
	def account(self, id: str) -> Account:
		account = table.query(
			KeyConditionExpression=Key('id').eq(id)
		)['Items']
		if not account:
			raise Exception('account not found')
		account = account[0]
		return Account.from_row(account)
