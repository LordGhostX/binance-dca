import json
from binance.client import Client

config = json.load(open("config.json"))
amount, fee = config["amount"], config["fee"]
client = Client(config["keys"]["api"], config["keys"]["secret"])
coins = config["coins"]


def init_dca():
    validate_distributions()
    print(f"Purchase Amount: ${amount:.2f}\nFee Rate: ${fee / 100 * amount:.2f}\n")

    for coin in coins:
        purchasing_amount = coins[coin] / 100 * amount
        total_purchase_amount = purchasing_amount + (fee / 100 * purchasing_amount)
        print(f"Attempting to buy ${total_purchase_amount:.2f} of ${coin.upper()}")
        place_order(coin, total_purchase_amount)


def validate_distributions():
    percentage = 0

    for coin in coins:
        percentage += coins[coin]

    if percentage != 100:
        raise ValueError("Coins allocation must add up to exactly 100")


def place_order(ticker, amount):
    if config["testing"]:
        create_order = client.create_test_order
    else:
        create_order = client.create_order

    res = create_order(
        symbol=f"{ticker}USDT".upper(),
        side=Client.SIDE_BUY,
        type=Client.ORDER_TYPE_MARKET,
        quoteOrderQty=round(amount, 3),
    )

    if config["testing"]:
        print("Real orders cannot be made in testing mode")
    else:
        print(
            f"Amount Bought: {res['executedQty']}\nPrice: ${1 / float(res['executedQty']) * float(res['cummulativeQuoteQty'])}\nTotal Spent: ${res['cummulativeQuoteQty']}\n\n"
        )


if __name__ == "__main__":
    init_dca()
