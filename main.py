# Para programarlo he buscado la formula del rebalance en google
# se calcula en total de dinero, se calcula en objetio se sacan las diferencias y se vende o compra segun
# la "distribution" que se pase a la clase Portfolio


class Stock:
    def __init__(self, name: str, amount: float) -> None:
        self.name = name
        self.amount = amount

    def get_current_price(self, price):
        return price


class Portfolio:
    def __init__(self) -> None:
        self.stocks = []
        self.distribution = {}

    def add_stock(self, stock: Stock) -> None:
        self.stocks.append(stock)

    def set_distribution(self, distribution):
        if sum(distribution.values()) != 1:
            raise ValueError("This config is not valid")
        self.distribution = distribution
        return self

    def rebalance(self, market_prices):
        rebalances = []

        total_money = sum(market_prices[s.name] * s.amount for s in self.stocks)

        for name, rate in self.distribution.items():
            target_value = rate * total_money
            stock = next((s for s in self.stocks if s.name == name), None)

            current_price = market_prices[name]

            current_value = (stock.amount * current_price) if stock else 0
            diff_amount = target_value - current_value

            if abs(diff_amount) > 0.01:
                stock_to_move = diff_amount / current_price
                action = "buy" if diff_amount > 0 else "sell"

                rebalances.append(
                    {
                        "name": name,
                        "action": action,
                        "stock_to_move": round(abs(stock_to_move), 4),
                        "amount": round(abs(diff_amount), 2),
                    }
                )
        return rebalances


porfolio = Portfolio()

porfolio.add_stock(Stock("LG", 10))

porfolio.add_stock(Stock("SONY", 60))

market_prices = {"SONY": 500.0, "LG": 200.0}

distribution = {"SONY": 0.7, "LG": 0.3}

result = porfolio.set_distribution(distribution).rebalance(market_prices)

print(result)
