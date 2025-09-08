import logging
import re
from BexarLandMine.HTML.Node import HTMLNode
from BexarLandMine.Data import DB
from datetime import date

logger = logging.getLogger(__name__)


class Detail():
    """Property detail page

    This should not be created directly. The constructor creates only an empty
    instance. Instead use the detail_from_html_node to instantiate instances.
    """
    node_filters = [
            (
                'account_number_node',
                'Account Number:'
            ),
            (
                'owner_address_node',
                'Address:'
            ),
            (
                'property_address_node',
                'Property Site Address:'
            ),
            (
                'legal_description_node',
                'Legal Description:'
            ),
            (
                'current_year_tax_levy_node',
                '2024 Year Tax Levy:'
            ),
            (
                'delinquent_amount_due_node',
                'Prior Year(s) Amount Due:'
            ),
            (
                'last_payment_amount_node',
                'Last Payment Amount Received:'
            ),
            (
                'last_payer_node',
                'Last Payer:'
            ),
            (
                'last_payment_amount_node',
                'Last Payment Date:'
            ),
            (
                'is_payment_pending_node',
                'Pending Credit Card or eCheck Payments:'
            ),
            (
                'total_market_value_node',
                'Total Market Value:'
            ),
            (
                'land_value_node',
                'Land Value:'
            ),
            (
                'improvement_value_node',
                'Improvement Value:'
            ),
            (
                'capped_value_node',
                'Capped Value:'
            ),
            (
                'ag_value_node',
                'Agricultural Value:'
            ),
            (
                'current_exemptions_node',
                'Exemptions (current year only):'
            ),
            (
                'current_jurisdictions_node',
                'Jurisdictions (current year only):'
            ),
            (
                'current_year',
                None
            ),
        ]

    def __init__(self, detail_html: HTMLNode):
        data_nodes: dict[str, HTMLNode] = {}
        self._account_number: int = 0
        self.owner_address: str = None
        self.property_address: str = None
        self.legal_description: str = None
        self.current_year: int = 0
        self.current_year_tax_levy: int = 0
        self.current_due_date: date = date.today()
        self.delinquent_amount_due: int = 0
        self.last_payment_amount: int = 0
        self.last_payer: str = None
        self.last_payment_date: date = date.today()
        self.is_payment_pending: bool = False
        self.total_market_value: int = 0
        self.land_value: int = 0
        self.improvement_value: int = 0
        self.capped_value: int = 0
        self.ag_value: int = 0
        self.current_exemptions: str = None
        self.current_jurisdictions: str = None
        try:
            body_node = find_html_body(detail_html)
        except ValueError:
            body_node = detail_html

        for key, search_str in self.node_filters:
            for node in body_node:
                match key:
                    case 'current_year':
                        if filter_year_table(node):
                            year = get_year_from_node(node)
                            if year:
                                self.current_year = year
                            break
                    case _:
                        if filter_detail_table(node, search_str):
                            data_nodes[key] = node
                            break
        for key, node in data_nodes.items():
            match key:
                case 'account_number_node':
                    self._account_number = int(node.children[1].value)
                case 'owner_address_node':
                    self.owner_address = node.children[1].value
                case 'property_address_node':
                    self.property_address = node.children[1].value
                case 'legal_description_node':
                    self.legal_description = node.children[1].value
                case 'current_year_tax_levy_node':
                    float_amount = float(node.children[1].value.removeprefix('$'))
                    self.current_year_tax_levy = self._convert_float_to_cent(float_amount)
                case 'delinquent_amount_due_node':
                    float_amount = float(node.children[1].value.removeprefix('$'))
                    self.delinquent_amount_due = self._convert_float_to_cent(float_amount)
                case 'last_payment_amount_node':
                    payment_str = node.children[1].value
                    if payment_str == 'Not Received':
                        pass
                    else:
                        float_amount = float(payment_str.removeprefix('$'))
                        self.last_payment_amount = self._convert_float_to_cent(float_amount)
                case 'last_payer_node':
                    self.last_payer = node.children[1].value
                case 'last_payment_date_node':
                    self.last_payment_date = date(node.children[1].value)
                case 'is_payment_pending_node':
                    self.is_payment_pending = bool(node.children[1].value)
                case 'total_market_value_node':
                    float_amount = float(node.children[1].value.removeprefix('$'))
                    self.total_market_value = self._convert_float_to_cent(float_amount)
                case 'improvement_value_node':
                    float_amount = float(node.children[1].value.removeprefix('$'))
                    self.improvement_value = self._convert_float_to_cent(float_amount)
                case 'land_value_node':
                    float_amount = float(node.children[1].value.removeprefix('$'))
                    self.land_value = self._convert_float_to_cent(float_amount)
                case 'capped_value_node':
                    float_amount = float(node.children[1].value.removeprefix('$'))
                    self.capped_value = self._convert_float_to_cent(float_amount)
                case 'ag_value_node':
                    float_amount = float(node.children[1].value.removeprefix('$'))
                    self.ag_value = self._convert_float_to_cent(float_amount)
                case 'current_exemptions_node':
                    self.current_exemptions = node.children[1].value
                case 'current_jurisdictions_node':
                    self.current_jurisdictions = node.children[1].value
                case _:
                    raise ValueError(f"Unknown key: {key}")

    def _convert_float_to_cent(self, amount_float: float) -> int:
        """Converts floating point money values to integer cent values."""
        return int(amount_float * 100)

    def total_ammount_due(self):
        return self.current_amount_due + self.delinquent_amount_due

    def write_db(self, db: DB, is_valid: bool):
        # owner_number_cur = db.get_owner(self.owner_address)
        # if not owner_number_cur:
        #     breakpoint()
        #     raise ValueError("Owner not in database")
        # owner_number, = owner_number_cur.fetchone()
        db.add_account(self._account_number, is_valid,
                       self.property_address, self.legal_description,
                       exemptions=self.current_exemptions,
                       jurisdictions=self.current_jurisdictions)
        db.add_owner(self._account_number, self.current_year,
                     self.owner_address)
        db.add_amounts(self._account_number, self.current_year,
                       self.current_year_tax_levy, self.delinquent_amount_due,
                       self.last_payment_amount, self.total_market_value,
                       self.land_value, self.improvement_value,
                       self.capped_value, self.ag_value)

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


def filter_detail_table(node, filter_str):
    return (node.tag == 'div'
            and len(node.children) == 2
            and node.children[0].tag == 'label'
            and len(node.children[0].children) == 1
            and node.children[0].children[0].value == filter_str)


def filter_year_table(node):
    return (node.tag == 'p'
            and len(node.children) == 1
            and node.children[0].tag == 'label'
            and len(node.children[0].children) == 1
            and not node.children[0].children[0].tag)


def get_year_from_node(node):
    re_str = r".*ALL DATA REFERS TO TAX INFORMATION FOR (P?<year>\d\d\d\d).*"
    year_re = re.compile(re_str)
    match = year_re.search(node.children[0].children[0].value)
    if match:
        return int(match.group('year'))
    return None


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


