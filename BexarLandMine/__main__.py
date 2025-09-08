import logging
from time import sleep
from random import randint
from requests import post
from BexarLandMine.Config import Config
from BexarLandMine.Data import DB
from BexarLandMine.HTML.Parser import BexarHTMLParser
from BexarLandMine.Land import Detail
logger = logging.getLogger(__name__)


def main():
    LOG_FORMAT = '%(asctime)s %(levelname)s %(message)s'
    conf = Config("config.toml")
    logging.basicConfig(filename=conf.data["output"]["logfile"],
                        level=logging.DEBUG, format=LOG_FORMAT)
    db = DB(conf.data["output"]["dbfile"])
    try:
        account_cur = db.get_last_account_number()
        start, = account_cur.fetchone()
        account_cur.close()
    except Exception as e:
        logger.error(str(e))
        start = 0

    for num in range(start + 1, conf.data["search"]["end"]):
        sleep(randint(1, conf.data["search"]["delay_seconds"]))
        data = f"can={num:012}"
        is_valid = True
        parser = BexarHTMLParser()
        url = f"{conf.data["bexar_details_url"]}?{data}"
        logger.info(f"Getting: {url}")
        res = post(url, headers=conf.data["headers"], data=data)
        html = res.text.strip()
        try:
            parser.feed(html)
        except ValueError:
            is_valid = False
            logger.info(f"account number '{num}' does not exist")
            db.add_invalid_account(num)
            continue
        try:
            page_detail = Detail(parser.root_node)
        except ValueError as e:
            print(e)
        else:
            logger.info(f"Page for account {num:012} parsed")
        try:
            page_detail.write_db(db, is_valid)
        except Exception as e:
            logger.error(str(e))


if __name__ == '__main__':
    main()
