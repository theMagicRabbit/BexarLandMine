import logging
from BexarLandMine.HTML.Node import HTMLNode
from datatime import date

logger = logging.getLogger(__name__)


class Detail():
    """Property detail page

    This should not be created directly. The constructor creates only an empty
    instance. Instead use the detail_from_html_node to instantiate instances.
    """

    def __init__(self, account_number: int):
        self.account_number: int = account_number
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

    def __repr__(self):
        return "Detail()"


def detail_from_html_node(html_node: HTMLNode) -> Detail:
    """Creates a detail instance from html node of property detail page"""
    account_number = 0
    detail = Detail(account_number)
    return detail
