
import random
import math

# TODO: Store these in a json file
stock_types = [
	dict(stockID="BNS", name="Bones", Value=1.23),
	dict(stockID="BBN", name="Baby Bones", Value=3.45)
]

# Value range as factor of base value
min_value = 0.01
max_value = 10

# How many random influences there will be
influence_value_count = 4

# Max and min values of an influence
min_influence = 0.95
max_influence = 1.05

# How many influences can influence one stock at once
min_stock_influence_count = 1
max_stock_influence_count = 5

# How many influences can influence one influence at once
min_influence_influence_count = 3
max_influence_influence_count = 4

# How much an influence can change randomly
min_influence_change = -0.1
max_influence_change =  0.1

# How many influences can change at once
influence_change_count = 10

# How frequently do influences change on their own (1/this value = freq of change)
influence_change_freq = 5


# Generate influence values and their inner-links
influence_values = []
for i in range(influence_value_count):
	# initial_influence_value = random.uniform(
		# min_influence, max_influence)
	initial_influence_value = 1.0

	nb_influences = random.randint(
		min_influence_influence_count,
		max_influence_influence_count)
	print("Number of influences: {}".format(nb_influences))

	# Generate links
	links = []
	for j in range(nb_influences):
		influence_id = random.randint(0, influence_value_count-1)
		links.append(influence_id)

	influence_values.append(dict(
		Id=i,
		Value=initial_influence_value,
		Links=links))


# Generate influence-stock links
stock_values = []
for stock in stock_types:
	new_stock = stock.copy()

	nb_influences = random.randint(
		min_stock_influence_count,
		max_stock_influence_count)

	links = []
	for j in range(nb_influences):
		influence_id = random.randint(0, influence_value_count-1)
		links.append(influence_id)

	new_stock.update(dict(Links=links))
	stock_values.append(new_stock)


def update_influences():
	for influence in influence_values:

		value_change = 1.0
		for influence_id in influence["Links"]:
			value_change *= influence_values[influence_id]["Value"]

		influence["Value"] *= value_change

		if influence["Value"] > max_influence:
			influence["Value"] = max_influence
		elif influence["Value"] < min_influence:
			influence["Value"] = min_influence


def update_stocks():
	for stock in stock_values:

		value_change = 1.0
		for influence_id in stock["Links"]:
			value_change *= influence_values[influence_id]["Value"]

		stock["Value"] *= value_change


def change_influences():
	for i in range(influence_change_count):
		influence_id = random.randint(0, influence_value_count-1)

		influence_values[influence_id]["Value"] += random.uniform(
			min_influence_change,
			max_influence_change)


def main_loop(time_units):
	for i in range(time_units):
		if i % influence_change_freq == 0:
			change_influences()
		
		update_influences()
		update_stocks()


main_loop(2000)

for influence in influence_values:
	print(influence["Value"])
print(stock_values)
