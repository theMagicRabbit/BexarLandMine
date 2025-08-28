import pytest
from BexarLandMine.HTML.Parser import BexarHTMLParser
from BexarLandMine.HTML.Node import LeafNode, ParentNode


def test_parse_html():
    tests = [
            (
                """<html>This is text in html tags.</html>""",
                ParentNode('html',
                           [LeafNode(None, 'This is text in html tags.')])
            ),
            (
                """<html><div>This is text in html tags.</div></html>
""",
                ParentNode(
                   'html', [
                        ParentNode('div', [
                            LeafNode(None, "This is text in html tags."),]),])
            ),
            (
                # Some tags have numbers in the tag name
                """<html><h1>This is text in html tags.</h1></html>
""",
                ParentNode(
                    'html', [
                        ParentNode('h1', [
                            LeafNode(None, "This is text in html tags."),]),])
            ),
            (
                """
<html><div>This is text in html tags.</div></html>
""",
                ParentNode(
                    'html', [
                        ParentNode('div', [
                            LeafNode(None, "This is text in html tags."),
                            ]),])
            )
        ]
    for input, expected in tests:
        parser = BexarHTMLParser()
        parser.feed(input)
        result = parser.root_node
        assert result == expected
