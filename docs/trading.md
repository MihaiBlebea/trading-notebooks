## Get S&P 500 month to month growth

Define the functions that we will need to use


```python
from __future__ import annotations
import yfinance as yf
import pandas as pd


def get_closing_prices(symbols: list)-> pd.Series | None:
    try:
        data = yf.download(
            symbols,
            interval="1mo",
            start="2021-01-01",
            end=f"2022-01-01",
            auto_adjust=True,
            rounding=True,
            progress=False,
            prepost=True,
        )
        return data.loc[:, "Close"].dropna()
    except:
        return None

def calc_percentage_diff(start_price: float, end_price: float)-> float:
    return round(end_price * 100 / start_price - 100, 2)

def get_stocks_list()-> list:
    table=pd.read_html("https://en.wikipedia.org/wiki/List_of_S%26P_500_companies")
    return list(table[0].to_dict()["Symbol"].values())

```

## How will this work? 

**Step by step:**

- Get the S&P 500 ticker symbol closing price per year. For this example we will use IVV

- Get all the stocks that make the S&P 500 ETF

- Get the closing prices per month for each of the S&P 500 stocks

- Determine which of the stocks that make the S&P 500 overperform against the ETF and which underperform


```python
symbols = get_stocks_list()
```


```python
# for symbol in symbols:
appl_prices = get_closing_prices(["AAPL"])
```

Calculate the difference from the first month to the last month in percentage


```python
prices = appl_prices.to_list()
start_price = prices[0]
last_price = prices[-1]
aapl_growth = calc_percentage_diff(start_price, last_price)

print(f"Last year growth for AAPL between 1st of Jan 2021 and 1st of Jan 2022 was {aapl_growth}%")
```

    Last year growth for AAPL between 1st of Jan 2021 and 1st of Jan 2022 was 35.39%


Calculate the growth rate of the S&P 500 over the period of last year


```python
closing_prices = get_closing_prices("IVV")
prices = closing_prices.to_list()
start_price = prices[0]
last_price = prices[-1]
benchmark_growth = calc_percentage_diff(start_price, last_price)

print(f"IVV growth over the past year was {benchmark_growth}%")
```

    IVV growth over the past year was 29.69%


Get all the symbols in S&P which outperform the fund


```python
from termcolor import colored

overs = []
unders = []

for symbol in symbols:
	prices = get_closing_prices([symbol])
	if prices is None:
		continue

	prices = prices.to_list()
	if len(prices) == 0:
		continue

	symbol_growth = calc_percentage_diff(prices[0], prices[-1])

	if symbol_growth > benchmark_growth:
		overs.append((symbol, symbol_growth))
	else:
		unders.append((symbol, symbol_growth))

print(colored(f"There are {len(overs)} companies that performed better than the market", "green"))
print(colored(f"There are {len(unders)} companies that performed worst than the market", "red"))
```

    
    1 Failed download:
    - BRK.B: No data found, symbol may be delisted
    
    1 Failed download:
    - BF.B: No data found for this date range, symbol may be delisted
    
    1 Failed download:
    - CEG: Data doesn't exist for startDate = 1609459200, endDate = 1640995200
    [32mThere are 250 companies that performed better than the market[0m
    [31mThere are 252 companies that performed worst than the market[0m


### Top 5 over performers from last year

First let's create a function that receives a list of symbols and returns back the yahoo finance tickers.

We don't want to fetch the extra data if we are not going to use it.


```python
import yfinance as yf
from typing import List, Tuple

def fetch_tickers(symbols: List[Tuple[str, float]])-> yf.Ticker:
	symbols = [ o[0] for o in symbols ]
	return [t.info for i, t in yf.Tickers(symbols).tickers.items()]
```


```python
top = 3
overs = sorted(overs, reverse=True, key=lambda x: x[1])
top_overs = overs[0:top]
tickers = fetch_tickers(top_overs)

for i, o in enumerate(top_overs):
	company_name = tickers[i]["longName"]
	print(colored(f"{i + 1}. {company_name} {o[0]} growth {o[1]}%", "green"))

```

    [32m1. Devon Energy Corporation DVN growth 178.94%[0m
    [32m2. Fortinet, Inc. FTNT growth 148.29%[0m
    [32m3. Nucor Corporation NUE growth 137.41%[0m


### Top 10 under performing stocks


```python
top = 10
unders = sorted(unders, reverse=False, key=lambda x: x[1])
top_unders = unders[0:top]
tickers = fetch_tickers(top_unders)

for i, o in enumerate(top_unders):
	company_name = tickers[i]["longName"]
	print(colored(f"{i + 1}. {company_name} {o[0]} growth {o[1]}%", "red"))
```

    [31m1. Penn National Gaming, Inc. PENN growth -50.01%[0m
    [31m2. Discovery, Inc. DISCA growth -43.17%[0m
    [31m3. Paramount Global PARA growth -36.87%[0m
    [31m4. Discovery, Inc. DISCK growth -34.63%[0m
    [31m5. Citrix Systems, Inc. CTXS growth -28.37%[0m
    [31m6. Activision Blizzard, Inc. ATVI growth -26.53%[0m
    [31m7. MarketAxess Holdings Inc. MKTX growth -23.52%[0m
    [31m8. Global Payments Inc. GPN growth -23.16%[0m
    [31m9. IPG Photonics Corporation IPGP growth -22.96%[0m
    [31m10. Las Vegas Sands Corp. LVS growth -21.73%[0m


### Check how the top performers and the top under performers ratios look like

- We are going to fetch the top 3 performers and top 10 under performers and just compare their ratios

- Ratios that we are going to consider:

	- P/E
	
	- EPS

	- Price/sales


```python
import yfinance as yf

TOP = 10

def round_it(value: str)-> float:
	return round(float(value), 2)

def select_and_sort(data: list, limit: int, reverse: bool = False)-> list:
	return sorted(data, reverse=reverse, key=lambda x: x[1])[0:limit]

top_overs = select_and_sort(overs, TOP, True)
top_unders = select_and_sort(unders, TOP)

data = {
	"Company": [],
	"Symbol": [],
	"Trailing P/E": [],
	"Forward P/E": [],
	"Growth": [],
}

for o in top_overs + top_unders:
	ticker = yf.Ticker(o[0])
	d = ticker.info
	data["Company"].append(d["longName"])
	data["Symbol"].append(o[0])
	if "trailingPE" not in d:
		data["Trailing P/E"].append("N/A")
	else:
		data["Trailing P/E"].append(round_it(d["trailingPE"]))
	data["Forward P/E"].append(round_it(d["forwardPE"]))
	data["Growth"].append(round_it(o[1]))

df = pd.DataFrame(data)
print(df)
```


    ---------------------------------------------------------------------------

    TypeError                                 Traceback (most recent call last)

    /home/mihaiblebea/Coding/Python/trading-notebooks/trading.ipynb Cell 19' in <cell line: 22>()
         <a href='vscode-notebook-cell:/home/mihaiblebea/Coding/Python/trading-notebooks/trading.ipynb#ch0000019?line=28'>29</a> 	else:
         <a href='vscode-notebook-cell:/home/mihaiblebea/Coding/Python/trading-notebooks/trading.ipynb#ch0000019?line=29'>30</a> 		data["Trailing P/E"].append(round_it(d["trailingPE"]))
    ---> <a href='vscode-notebook-cell:/home/mihaiblebea/Coding/Python/trading-notebooks/trading.ipynb#ch0000019?line=30'>31</a> 	data["Forward P/E"].append(round_it(d["forwardPE"]))
         <a href='vscode-notebook-cell:/home/mihaiblebea/Coding/Python/trading-notebooks/trading.ipynb#ch0000019?line=31'>32</a> 	data["Growth"].append(round_it(o[1]))
         <a href='vscode-notebook-cell:/home/mihaiblebea/Coding/Python/trading-notebooks/trading.ipynb#ch0000019?line=33'>34</a> df = pd.DataFrame(data)


    /home/mihaiblebea/Coding/Python/trading-notebooks/trading.ipynb Cell 19' in round_it(value)
          <a href='vscode-notebook-cell:/home/mihaiblebea/Coding/Python/trading-notebooks/trading.ipynb#ch0000019?line=4'>5</a> def round_it(value: str)-> float:
    ----> <a href='vscode-notebook-cell:/home/mihaiblebea/Coding/Python/trading-notebooks/trading.ipynb#ch0000019?line=5'>6</a> 	return round(float(value), 2)


    TypeError: float() argument must be a string or a number, not 'NoneType'

