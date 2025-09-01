import logging
from BexarLandMine.HTML.Node import HTMLNode
from datetime import date

logger = logging.getLogger(__name__)


class Detail():
    """Property detail page

    This should not be created directly. The constructor creates only an empty
    instance. Instead use the detail_from_html_node to instantiate instances.
    """

    def __init__(self, account_number: int):
        self._account_number: int = account_number
        self.owner_address: str = ""
        self.property_address: str = ""
        self.legal_description: str = ""
        self.current_year: int = 0
        self.current_tax_levy: float = 0.0
        self.current_amount_due: float = 0.0
        self.current_due_date: date = date.today()
        self.delinquent_amount_due: float = 0.0
        self.last_payment_amount: float = 0.0
        self.last_payer: str = ""
        self.last_payment_date: date = date.today()
        self.is_payment_pending: bool = False
        self.total_market_value: float = 0.0
        self.land_value: float = 0.0
        self.improvement_value: float = 0.0
        self.ag_value: float = 0.0
        self.current_exemptions: str = ""
        self.current_jurisdictions: str = ""
        logger.debug("Detail instance created")

    def total_ammount_due(self):
        return self.current_amount_due + self.delinquent_amount_due

    def account_number(self):
        """Pad the account number for web

        The ACT Tax site uses a 12 digit number padded with zeros as the 'can'
        or (to my best guess) 'County Account Number.' Before passing the
        account_number to the website, it needs to be padded into a string.
        """
        return f"{self._account_number:012}"

    def __repr__(self):
        return f"Detail({self._account_number})"

    def __eq__(self, o):
        return (self._account_number == o._account_number)


def filter_account_num(node):
    return (node.tag == 'div'
            and len(node.children) == 2
            and 'label' == node.children[0].tag
            and len(node.children[0].children) == 1
            and node.children[0].children[0].value == 'Account Number:'
            )


def find_html_body(html_node: HTMLNode) -> HTMLNode:
    """Find the body node in an html document

    Since the data should be in the body node and the body node should be
    a direct desendant of the top level html node, we can cut down on some
    remove some of the other high level nodes and save some processing time.
    """
    for node in html_node.children:
        if node.tag == 'body':
            return node
    raise ValueError("Body node not found")


def detail_from_html_node(html_node: HTMLNode) -> Detail:
    """Creates a detail instance from html node of property detail page"""
    account_number_node = None

    try:
        body_node = find_html_body(html_node)
    except ValueError:
        body_node = html_node

    for node in body_node:
        logger.debug(f"Checking for 'label' tag: {node}")
        if filter_account_num(node):
            account_number_node = node
            break
    if account_number_node:
        logger.debug(f"account_number_node: {account_number_node}")
        account_number = int(account_number_node.children[1].value)
    detail = Detail(account_number)
    return detail
