import json
from binance.client import Client

config = json.load(open("config.json"))
quote_asset, amount, fee = config["quote_asset"], config["amount"], config["fee"]
client = Client(config["keys"]["api"], config["keys"]["secret"])


def fetch_balance(asset):
    return float(client.get_asset_balance(asset=asset)["free"])


def place_order(ticker, amount):
    if config["testing"]:
        create_order = client.create_test_order
    else:
        create_order = client.create_order

    res = create_order(
        symbol=f"{ticker}{quote_asset}".upper(),
        side=Client.SIDE_BUY,
        type=Client.ORDER_TYPE_MARKET,
        quoteOrderQty=round(amount, 3)
    )

    if config["testing"]:
        print("Real orders cannot be made in testing mode")
    else:
        print(f"Amount Bought: {res['executedQty']}\nPrice: ${1 / float(res['executedQty']) * float(res['cummulativeQuoteQty'])}\nTotal Spent: ${res['cummulativeQuoteQty']}\n\n")


try:
    # check API key validity
    balance = fetch_balance(quote_asset)
    print(f"${quote_asset} Balance:", balance)
    print(
        f"Purchase Amount: ${amount:.2f}\nFee Rate: ${fee / 100 * amount:.2f}\n")
except:
    exit("invalid binance API key or config settings")

if amount > balance:
    exit(f"insufficient ${quote_asset} balance to run DCA")

if sum(config["coins"].values()) > 100:
    exit("asset allocation cannot exceed 100%")

coins = config["coins"]
for coin in coins:
    purchasing_amount = coins[coin] / 100 * amount
    total_purchase_amount = purchasing_amount + (fee / 100 * purchasing_amount)
    print(f"Attempting to buy ${total_purchase_amount:.2f} of ${coin.upper()}")
    place_order(coin, total_purchase_amount)
