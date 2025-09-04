import logging
from requests import post
from BexarLandMine.Config import Config
from BexarLandMine.Data import DB
from BexarLandMine.HTML.Parser import BexarHTMLParser
from BexarLandMine.Land import Detail
logger = logging.getLogger(__name__)


def main():
    LOG_FORMAT = '%(asctime)s %(levelname)s %(message)s'
    account_number = 1
    data = f"can={account_number:012}"
    conf = Config("config.toml")
    logging.basicConfig(filename=conf.data["output"]["logfile"],
                        level=logging.DEBUG, format=LOG_FORMAT)
    p = BexarHTMLParser()
    url = f"{conf.data["bexar_details_url"]}?{data}"
    logger.info(f"Getting: {url}")
    res = post(url, headers=conf.data["headers"], data=data)
    p.feed(res.text)
    try:
        d = Detail(p.root_node)
    except ValueError as e:
        print(e)
    else:
        print(d)
    d = DB(conf.data["output"]["dbfile"])


if __name__ == '__main__':
    main()
