from requests import post
from BexarLandMine.Config import Config

data = "searchby=5&criteria=000000"
conf = Config("config.toml")
res = post(conf.data["bexar_list_url"], headers=conf.data["headers"], data=data)
print(res.text)
