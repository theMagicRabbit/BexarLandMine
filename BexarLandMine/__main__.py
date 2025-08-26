from requests import post
from BexarLandMine.Config import Config
from BexarLandMine.HTML.Parser import DetailPageHTMLParser

account_number = 1
data = f"can={account_number:012}"
conf = Config("config.toml")
p = DetailPageHTMLParser()
url = f"{conf.data["bexar_details_url"]}?{data}"
print(f"Getting: {url}")
res = post(url, headers=conf.data["headers"], data=data)
p.feed(res.text)
