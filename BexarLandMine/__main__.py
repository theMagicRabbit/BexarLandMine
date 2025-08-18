from requests import post
from BexarLandMine.Config import Config
from BexarLandMine.Parser import MyHTMLParser

data = "searchby=5&criteria=000000"
conf = Config("config.toml")
p = MyHTMLParser()
res = post(conf.data["bexar_list_url"], headers=conf.data["headers"], data=data)
p.feed(res.text)
