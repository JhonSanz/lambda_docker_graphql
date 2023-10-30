import strawberry
import boto3
from boto3.dynamodb.conditions import Key
from type import Account
from utils import PaginationWindow, get_pagination_window
from db_query import AccountQuery
from filters import FilterManager

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('accounts')


@strawberry.type
class Query:
	@strawberry.field(description="Get a list of account")
	def accounts(
		self,
		order_by: str,
		limit: int,
		query: AccountQuery,
		offset: int = 0,
	) -> PaginationWindow[Account]:

		filters = FilterManager(query).generate()
		accounts = table.scan(**filters)
		accounts = accounts["Items"]

		return get_pagination_window(
			dataset=accounts,
			ItemType=Account,
			order_by=order_by,
			limit=limit,
			offset=offset,
		)

	@strawberry.field(description="Get a account record.")
	def account(self, id: str) -> Account:
		account = table.query(
			KeyConditionExpression=Key('id').eq(id)
		)['Items']
		if not account:
			raise Exception('account not found')
		account = account[0]
		return Account.from_row(account)
