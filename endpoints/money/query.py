import strawberry
import boto3
from boto3.dynamodb.conditions import Key
from type import Money
from utils import PaginationWindow, get_pagination_window
from db_query import MoneyQuery
from filters import FilterManager


dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('money')

@strawberry.type
class Query:
	@strawberry.field(description='Get a list of money')
	def moneys(
		self,
		order_by: str,
		limit: int,
		query: MoneyQuery,
		offset: int = 0,
	) -> PaginationWindow[Money]:
		filters = FilterManager(query).generate()
		moneys = table.scan(**filters)
		moneys = moneys['Items']
		return get_pagination_window(
			dataset=moneys,
			ItemType=Money,
			order_by=order_by,
			limit=limit,
			offset=offset,
		)

	@strawberry.field(description='Get a money record.')
	def money(self, id: str) -> Money:
		money = table.query(
			KeyConditionExpression=Key('id').eq(id)
		)['Items']
		if not money:
			raise Exception('money not found')
		money = money[0]
		return Money.from_row(money)
