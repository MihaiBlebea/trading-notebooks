## Dividend Yeld

The dividend yield, expressed as a percentage, is a financial ratio (dividend/price) that shows how much a company pays out in dividends each year relative to its stock price.

- The dividend yield—displayed as a percentage—is the amount of money a company pays shareholders for owning a share of its stock divided by its current stock price.

- Mature companies are the most likely to pay dividends.

- Companies in the utility and consumer staple industries often having higher dividend yields. 

- Real estate investment trusts (REITs), master limited partnerships (MLPs), and business development companies (BDCs) pay higher than average dividends; however, the dividends from these companies are taxed at a higher rate. 

- It's important for investors to keep in mind that higher dividend yields do not always indicate attractive investment opportunities because the dividend yield of a stock may be elevated as the result of a declining stock price. 

[Read more](https://www.investopedia.com/terms/d/dividendyield.asp)


```python
symbols = ["PEP", "KO"]
```


```python
import warnings
warnings.simplefilter(action="ignore", category=FutureWarning)

from yahoo_fin import stock_info
import pandas as pd


keys = [
	"Forward Annual Dividend Rate 4",
	"Forward Annual Dividend Yield 4",
	"Trailing Annual Dividend Rate 3",
	"Trailing Annual Dividend Yield 3",
	"Dividend Date 3",
	"Payout Ratio 4"
]

data = {}
for s in symbols:
	data[s] = []

for s in symbols:
	stats = stock_info.get_stats(s.upper())
	attributes = {v: k for k, v in stats.to_dict()["Attribute"].items()}
	data[s] = [ stats["Value"][attributes[k]] for k in keys ]

df = pd.DataFrame(data=data, index=keys)
print(df)
```

                                               PEP            KO
    Forward Annual Dividend Rate 4             4.3          1.76
    Forward Annual Dividend Yield 4          2.59%         2.84%
    Trailing Annual Dividend Rate 3           4.25          1.68
    Trailing Annual Dividend Yield 3         2.56%         2.71%
    Dividend Date 3                   Mar 30, 2022  Mar 31, 2022
    Payout Ratio 4                          77.37%        74.67%


## Calculate dividend amount in $ from these shares

How to calculate DPS (Dividend Per Share)?

DPS = EPS * DPR

DPS - Dividend per Share

EPS - Earnings per Share

DPR - Dividend Payout Ratio


```python
from lib.fundamentals import format_amount

stats_keys = [
	"Payout Ratio 4"
]

def get_payout_ratio(symbol: str)-> str:
	stats = stock_info.get_stats(symbol.upper())
	attributes = {v: k for k, v in stats.to_dict()["Attribute"].items()}
	payout_ratio = stats["Value"][attributes["Payout Ratio 4"]]
	
	return float(payout_ratio.replace("%", "")) / 100

def fmt_percentage_str(value: float)-> str:
	return f"{value * 100}%"

data = {}
for s in symbols:
	data[s] = []

for s in symbols:
	quote = stock_info.get_quote_data(s.upper())
	price = stock_info.get_live_price(s.upper())

	price = round(price, 2)

	eps_current = quote["epsCurrentYear"]
	eps_forward = quote["epsForward"]

	payout_ratio = get_payout_ratio(s.upper())
	data[s].append(fmt_percentage_str(payout_ratio))

	dps_current = round(eps_current * payout_ratio, 2)
	dps_forward = round(eps_forward * payout_ratio, 2)

	investment_needed = 0
	if dps_forward > 0:
		investment_needed = round(price * 500 / dps_forward, 2)

	data[s] = data[s] + [
		eps_current,
		eps_forward,
		format_amount(dps_current),
		format_amount(dps_forward),
		format_amount(price),
		format_amount(investment_needed)
	]


dividend_keys = [
	"EpsCurrentYear", 
	"EpsForward", 
	"DividendPerShareCurrent", 
	"DividendPerShareForward",
	"LivePrice",
	"For500Dividend"
]

df = pd.DataFrame(data=data, index=stats_keys + dividend_keys)
print(df)
```

                                    PEP          KO
    Payout Ratio 4               77.37%      74.67%
    EpsCurrentYear                 6.67        2.46
    EpsForward                     7.24        2.64
    DividendPerShareCurrent       $5.16       $1.84
    DividendPerShareForward        $5.6       $1.97
    LivePrice                   $167.47      $62.04
    For500Dividend           $14,952.68  $15,746.19

