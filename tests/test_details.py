from BexarLandMine.HTML.Node import HTMLNode
from BexarLandMine.Land import filter_detail_table, Detail


def test_filters():
    node_filters = [
            (
                'account_number_node',
            ),
            (
                'account_address_node',
                'Address:'
            ),
            (
                'property_address_node',
                'Property Site Address:'
            ),
        ]
    tests = [
        (
            (
                HTMLNode(tag='div', value=None, children=[
                    HTMLNode(tag='label', value=None, children=[
                        HTMLNode(tag=None, value='Account Number:',
                                 children=[])
                    ]),
                    HTMLNode(tag=None, value='000000000001', children=[])
                ]),
                'Account Number:'
            ),
            True
        ),
        (
            (
                HTMLNode(tag='div', value=None, children=[
                    HTMLNode(tag='label', value=None, children=[
                        HTMLNode(tag=None, value='Address:', children=[])
                    ]),
                    HTMLNode(tag=None, value='000000000001', children=[])
                ]),
                'Account Number:'
            ),
            False
        ),
        (
            (
                HTMLNode(tag='div', value=None, children=[
                    HTMLNode(tag='label', value=None, children=[
                        HTMLNode(tag=None, value='Address:', children=[])
                    ]),
                    HTMLNode(tag=None, value='000000000001', children=[])
                ]),
                'Account Number:'
            ),
            False
        ),
        (
            (
                HTMLNode(tag='div', value=None, children=[
                    HTMLNode(tag='label', value=None, children=[
                        HTMLNode(tag=None, value='Address:', children=[])
                    ]),
                ]),
                'Address:'
            ),
            False
        ),
        (
            (
                HTMLNode(tag='div', value=None, children=[]),
                'Address:'
            ),
            False
        ),
        (
            (
                HTMLNode(tag='div', value=None, children=[
                    HTMLNode(tag='label', value=None, children=[
                        HTMLNode(tag=None, value='Address:',
                                 children=[])
                    ]),
                    HTMLNode(tag=None, value='TEST ACCOUNT', children=[])
                ]),
                'Address:'
            ),
            True
        ),
    ]
    for input, expected in tests:
        result = filter_detail_table(*input)
        assert result == expected


def test_details():
    tests = [
        (
            HTMLNode(tag='div', value=None, children=[
                HTMLNode(tag='label', value=None, children=[
                    HTMLNode(tag=None, value='Account Number:', children=[])
                ]),
                HTMLNode(tag=None, value='000000000001', children=[])
            ]),
            '000000000001'
        ),
    ]
    for input, expected in tests:
        can = expected
        result = Detail(input)
        assert result.account_number() == can
