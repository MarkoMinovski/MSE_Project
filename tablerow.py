class TableRow:
    def __init__(self, values):
        self.date = values[0]
        self.last_trade_price = values[1]
        self.max = values[2]
        self.min = values[3]
        self.avg = values[4]
        self.percentage_change_as_decimal = values[5]
        self.volume = values[6]
        self.BEST_turnover_in_denars = values[7]
        self.total_turnover_in_denars = values[8]


