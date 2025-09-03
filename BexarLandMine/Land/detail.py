import logging
from BexarLandMine.HTML.Node import HTMLNode
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
                'current_year_amount_due_node',
                '2024 Year Amount Due:'
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
            )
        ]

    def __init__(self, detail_html: HTMLNode):
        data_nodes: dict[str, HTMLNode] = {}
        self._account_number: int = 0
        self.owner_address: str = ""
        self.property_address: str = ""
        self.legal_description: str = ""
        self.current_year: int = 0
        self.current_year_tax_levy: float = 0.0
        self.current_year_amount_due: float = 0.0
        self.current_due_date: date = date.today()
        self.delinquent_amount_due: float = 0.0
        self.last_payment_amount: float = 0.0
        self.last_payer: str = ""
        self.last_payment_date: date = date.today()
        self.is_payment_pending: bool = False
        self.total_market_value: float = 0.0
        self.land_value: float = 0.0
        self.improvement_value: float = 0.0
        self.capped_value: float = 0.0
        self.ag_value: float = 0.0
        self.current_exemptions: str = ""
        self.current_jurisdictions: str = ""
        logger.debug("Detail instance created")
        try:
            body_node = find_html_body(detail_html)
        except ValueError:
            body_node = detail_html

        for key, search_str in self.node_filters:
            for node in body_node:
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
                    self.current_year_tax_levy = float(node.children[1].value.removeprefix('$'))
                case 'current_year_amount_due_node':
                    self.current_year_amount_due = float(node.children[1].value.removeprefix('$'))
                case 'delinquent_amount_due_node':
                    self.delinquent_amount_due = float(node.children[1].value.removeprefix('$'))
                case 'last_payment_amount_node':
                    payment_str = node.children[1].value
                    if payment_str == 'Not Received':
                        pass
                    else:
                        self.last_payment_amount = float(payment_str
                                                         .removeprefix('$'))
                case 'last_payer_node':
                    self.last_payer = node.children[1].value
                case 'last_payment_date_node':
                    self.last_payment_date = date(node.children[1].value)
                case 'is_payment_pending_node':
                    self.is_payment_pending = bool(node.children[1].value)
                case 'total_market_value_node':
                    self.total_market_value = float(node.children[1].value.removeprefix('$'))
                case 'improvement_value_node':
                    self.improvement_value = float(node.children[1].value.removeprefix('$'))
                case 'land_value_node':
                    self.land_value = float(node.children[1].value.removeprefix('$'))
                case 'capped_value_node':
                    self.capped_value = float(node.children[1].value.removeprefix('$'))
                case 'ag_value_node':
                    self.ag_value = float(node.children[1].value.removeprefix('$'))
                case 'current_exemptions_node':
                    self.current_exemptions = node.children[1].value
                case 'current_jurisdictions_node':
                    self.current_jurisdictions = node.children[1].value
                case _:
                    breakpoint()
                    raise ValueError(f"Unknown key: {key}")

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


def filter_detail_table(node, filter_str):
    return (node.tag == 'div'
            and len(node.children) == 2
            and node.children[0].tag == 'label'
            and len(node.children[0].children) == 1
            and node.children[0].children[0].value == filter_str
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


