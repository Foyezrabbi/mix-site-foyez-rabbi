from pycoingecko import CoinGeckoAPI

cg = CoinGeckoAPI()


def get_price(url):
    row = url.replace("https://www.coingecko.com/en/coins/", "")

    coin_dict = cg.get_price(ids=row, vs_currencies='usd')  # find price

    for value in coin_dict.values():
        usd = f"${value.get('usd')}"
        return usd

print(get_price("bitcoin"))

