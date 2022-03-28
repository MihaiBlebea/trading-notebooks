from yahoo_fin import stock_info as stock
from lib.utils import format_amount
from pprint import pprint

def book_value(symbol: str)-> dict:
	df = stock.get_balance_sheet(symbol.upper())

	for k, v in sorted(df.to_dict().items()):
		l = v["totalCurrentLiabilities"]
		a = v["totalCurrentAssets"]
		yield {
			"year": k.year,
			"total_liabilities": l,
			"total_assets": a,
			"book": a - l
		}

def free_cashflow(symbol: str)-> dict:
	df = stock.get_cash_flow(symbol.upper())
	for k, v in sorted(df.to_dict().items()):
		free_cf = v["totalCashFromOperatingActivities"] - v["capitalExpenditures"]
		yield {
			"year": k.year,
			"free_cashflow": free_cf,
		}

def discounted_cashflow_value(symbol: str, growth_rate: float, years: int, discount_rate: float)-> float:
	"""
	symbol - the ticket you want to analyse

	growth_rate - percentage of growth year by year that we expect the company to grow ex 5% = 0.05

	year - number of years that we want to look into the future

	discount_rate - percentage of discount that we want to apply to future cash flow ex 5% = 0.05
	"""
	last_cf = list(free_cashflow(symbol.upper()))[-1]["free_cashflow"]
	dcf = 0
	for i in range(1, years + 1, 1):
		dcf += last_cf + (last_cf * growth_rate * i) / (1 + discount_rate)**i

	return round(dcf)


if __name__ == "__main__":
	# for s in free_cashflow("AAPL"):
	# 	pprint(s)

	val = discounted_cashflow_value("aapl", 0.05, 5, 0.05)
	print(format_amount(val))