from BexarLandMine.HTML.Node import HTMLNode
from BexarLandMine.Land import filter_account_num


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
    ]
    for input, expected in tests:
        result = filter_account_num(input)
        assert result == expected
