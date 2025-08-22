from requests import post
from BexarLandMine.Config import Config
from BexarLandMine.HTML.Parser import ResultListHTMLParser

data = "searchby=5&criteria=000000"
conf = Config("config.toml")
p = ResultListHTMLParser()
res = post(conf.data["bexar_list_url"],
           headers=conf.data["headers"], data=data)
p.feed(res.text)
