
class server_settings:
	bind_ip = "0.0.0.0"
	bind_port = 9999


class client_settings:
	bind_ip = "0.0.0.0"
	bind_port = 9999


class market_settings:
	stock_types_filepath = "data/stock_types.json"

	# How many days history of each stock should we store
	price_history_len = 100

	# Mean trend /255 of change
	mean = 0.1

	# Stdev trend /sqrt(225) of change
	stdev = 0.3

	# How many updates until mean/stdev change
	update_period = 25

	# Time between updates (in seconds)
	update_delay = 1