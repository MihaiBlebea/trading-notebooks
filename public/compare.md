# Which one should I invest in?

- Current Ratio - should be greater than 1.5 - it compares the current assets against the current liabilities

- Price / Book Ratio (P/B) - should be < 3 - shows the difference between the market value of a company and its current value

- PEG Ratio - should be < 1 (means great) or < 3 (means good) - PEG less than one is considered undervalued, as the price is low compared to the company's expected earnings growth. Like P/E but including the growth factor.

- Dividends Payout - should be < 60% (0.6) - highlights if the company will be able to pay its dividends to shareholders.


```python
import warnings
warnings.simplefilter(action="ignore", category=FutureWarning)

from yahoo_fin import stock_info
import pandas as pd
from pprint import pprint

symbols = ["NVDA", "AMD", "INTC", "TSLA"]

keys = [
	"52 Week High 3", 
	"52 Week Low 3",
	"52-Week Change 3",
	"S&P500 52-Week Change 3",
	"Beta (5Y Monthly)",
	"Current Ratio (mrq)", 
	"Operating Cash Flow (ttm)", 
	"Quarterly Revenue Growth (yoy)",
	"Revenue Per Share (ttm)",
	"Payout Ratio 4",
	"Book Value Per Share (mrq)",
	"Operating Margin (ttm)",
	"Profit Margin",
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

                                       NVDA     AMD     INTC     TSLA
    52 Week High 3                   346.47  164.46    68.49  1243.49
    52 Week Low 3                    127.05   72.50    43.63   546.98
    52-Week Change 3                119.23%  58.21%  -19.23%   71.78%
    S&P500 52-Week Change 3          14.71%  14.71%   14.71%   14.71%
    Beta (5Y Monthly)                  1.41    1.85     0.55     2.05
    Current Ratio (mrq)                6.65    2.02     2.10     1.38
    Operating Cash Flow (ttm)         9.11B   3.52B   29.99B    11.5B
    Quarterly Revenue Growth (yoy)   52.80%  48.80%    2.80%   64.90%
    Revenue Per Share (ttm)           10.78   13.55    19.47    54.59
    Payout Ratio 4                    4.16%   0.00%   28.60%    0.00%
    Book Value Per Share (mrq)        10.62    6.21    23.44    29.23
    Operating Margin (ttm)           37.31%  22.20%   27.94%   12.12%


## Revenue Per Share

- Sales per share is a financial ratio that measures the total revenue earned per share over a specific time period.

- To calculate sales per share, divided total revenue by the average total shares outstanding.

- Sales per share provides a quick glance in identifying a company's productivity per share outstanding. The higher the sales-per-share ratio, the better a company is typically performing.

- Investors and analysts use sales per share to compare companies in a similar sector and to compare how the company is performing over different periods of time.

- Sales per share can be a limiting number as it only provides insight into a company's revenues, and does not take into consideration any debt or expenses on how those revenues were achieved.

[Read more](https://www.investopedia.com/terms/s/salespershare.asp)

## Beta

Beta is a measure used in fundamental analysis to determine the volatility of an asset or portfolio in relation to the overall market. The overall market has a beta of 1.0, and individual stocks are ranked according to how much they deviate from the market.

A stock that swings more than the market over time has a beta greater than 1.0. If a stock moves less than the market, the stock's beta is less than 1.0. High-beta stocks tend to be riskier but provide the potential for higher returns. Low-beta stocks pose less risk but typically yield lower returns.

As a result, beta is often used as a risk-reward measure, meaning it helps investors determine how much risk they are willing to take to achieve the return for taking on that risk. A stock's price variability is important to consider when assessing risk. If you think of risk as the possibility of a stock losing its value, beta is useful as a proxy for risk.

Essentially, beta expresses the trade-off between minimizing risk and maximizing return. Say a company has a beta of 2. This means it is two times as volatile as the overall market. We expect the market overall to go up by 10%. That means this stock could rise by 20%. On the other hand, if the market declines 6%, investors in that company can expect a loss of 12%.

[Read more](https://www.investopedia.com/ask/answers/070615/what-formula-calculating-beta.asp)

## Payout Ratio

*(Or dividend payout ratio)*

The payout ratio is a financial metric showing the proportion of earnings a company pays its shareholders in the form of dividends, expressed as a percentage of the company's total earnings. On some occasions, the payout ratio refers to the dividends paid out as a percentage of a company's cash flow. The payout ratio is also known as the dividend payout ratio.

- The payout ratio, also known as the dividend payout ratio, shows the percentage of a company's earnings paid out as dividends to shareholders.

- A low payout ratio can signal that a company is reinvesting the bulk of its earnings into expanding operations.

- A payout ratio over 100% indicates that the company is paying out more in dividends than its earning can support, which some view as an unsustainable practice.

[Read more](https://www.investopedia.com/terms/p/payoutratio.asp)

## Book Value Per Share

- Book value per share (BVPS) takes the ratio of a firm's common equity divided by its number of shares outstanding.

- Book value of equity per share effectively indicates a firm's net asset value (total assets - total liabilities) on a per-share basis.

- When a stock is undervalued, it will have a higher book value per share in relation to its current stock price in the market.

- BVPS is used mainly by stock investors to evaluate a company's stock price.

[Read more](https://www.investopedia.com/terms/b/bvps.asp)

## Operating Margin

The operating margin measures how much profit a company makes on a dollar of sales after paying for variable costs of production, such as wages and raw materials, but before paying interest or tax. It is calculated by dividing a company’s operating income by its net sales. Higher ratios are generally better, illustrating the company is efficient in its operations and is good at turning sales into profits.

- The operating margin represents how efficiently a company is able to generate profit through its core operations.

- It is expressed on a per-sale basis after accounting for variable costs but before paying any interest or taxes (EBIT).

- Higher margins are considered better than lower margins, and can be compared between similar competitors but not across different industries.

- To calculate the operating margin, divide operating income (earnings) by sales (revenues).

[Read more](https://www.investopedia.com/terms/o/operatingmargin.asp)

## Profit Margin

Profit margin is one of the commonly used profitability ratios to gauge the degree to which a company or a business activity makes money. It represents what percentage of sales has turned into profits. Simply put, the percentage figure indicates how many cents of profit the business has generated for each dollar of sale. For instance, if a business reports that it achieved a 35% profit margin during the last quarter, it means that it had a net income of $0.35 for each dollar of sales generated.

- Profit margin gauges the degree to which a company or a business activity makes money, essentially by dividing income by revenues.

- Expressed as a percentage, profit margin indicates how many cents of profit has been generated for each dollar of sale.

- While there are several types of profit margin, the most significant and commonly used is net profit margin, a company’s bottom line after all other expenses, including taxes and one-off oddities, have been removed from revenue.

- Profit margins are used by creditors, investors, and businesses themselves as indicators of a company's financial health, management's skill, and growth potential.

- As typical profit margins vary by industry sector, care should be taken when comparing the figures for different businesses.

[Read more](https://www.investopedia.com/terms/p/profitmargin.asp)
