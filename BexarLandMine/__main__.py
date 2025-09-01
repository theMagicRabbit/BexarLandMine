import logging
from requests import post
from BexarLandMine.Config import Config
from BexarLandMine.HTML.Parser import BexarHTMLParser
from BexarLandMine.Land import detail_from_html_node
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
    for node in p.root_node:
        print(node)
    #detail_from_html_node(p.root_node)


if __name__ == '__main__':
    main()
