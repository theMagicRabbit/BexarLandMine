from requests import get
from BexarLandMine.Config import Config

conf = Config("config.toml")
print(get(conf.data["bexar_index_url"]).text)
