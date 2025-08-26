from html.parser import HTMLParser
from BexarLandMine.HTML.Node import HTMLNode


class DetailPageHTMLParser(HTMLParser):
    def __init__(self):
        self.html_node = None
        super().__init__()

    def __repr__(self):
        return "DetailPageHTMLParser()"

    def handle_starttag(self, tag, attrs):
        if tag == 'script':
            return
        node = HTMLNode(tag)
        if not self.html_node:
            self.html_node = node
        else:
            self.html_node.children.append(node)

    def handle_data(self, data):
        print(data)
