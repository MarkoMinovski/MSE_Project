from tablerow import TableRow


class Table:
    def __init__(self, ticker):
        self.ticker = ticker
        self.TableEntries = []

    def AddToTableEntries(self, values):
        self.TableEntries.append(TableRow(values))