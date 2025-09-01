from BexarLandMine.HTML.Node import HTMLNode
from BexarLandMine.Land import filter_account_num, Detail, detail_from_html_node


def test_filter_account_num():
    tests = [
        (
            HTMLNode(tag='div', value=None, children=[
                HTMLNode(tag='label', value=None, children=[
                    HTMLNode(tag=None, value='Account Number:', children=[])
                ]),
                HTMLNode(tag=None, value='000000000001', children=[])
            ]),
            True
        ),
        (
            HTMLNode(tag='div', value=None, children=[
                HTMLNode(tag='label', value=None, children=[
                    HTMLNode(tag=None, value='Address:', children=[])
                ]),
                HTMLNode(tag=None, value='Test Account', children=[])
            ]),
            False
        ),
        (
            HTMLNode(tag='div', value=None, children=[
                HTMLNode(tag='label', value=None, children=[
                ]),
                HTMLNode(tag=None, value='Test Account', children=[])
            ]),
            False
        ),
        (
            HTMLNode(tag='div', value=None, children=[]),
            False
        ),
    ]
    for input, expected in tests:
        result = filter_account_num(input)
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
            (Detail(1), '000000000001')
        ),
    ]
    for input, expected in tests:
        node, can = expected
        result = detail_from_html_node(input)
        assert result == node
        assert result.account_number() == can
