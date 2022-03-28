def format_amount(value: float)-> str:
	return "${:,}".format(value)

def calculate_growth_rate(initial: float, last: float)-> float:
	diff = (last - initial) / initial * 100
	return round(diff)