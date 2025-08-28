from html.parser import HTMLParser
from BexarLandMine.HTML.Node import ParentNode, LeafNode


class BexarHTMLParser(HTMLParser):
    def __init__(self):
        self.tag_stack = []
        self.node_stack = []
        self.children_nodes = []
        self.root_node = None
        super().__init__()

    def __repr__(self):
        return "BexarHTMLParser()"

    def feed(self, data: str):
        cleaned = data.strip()
        super().feed(cleaned)

    def handle_starttag(self, tag, attrs):
        self.tag_stack.append(tag)
        self.children_nodes.append([])

    def handle_endtag(self, tag):
        try:
            pop_tag = self.tag_stack.pop()
        except IndexError:
            print("tag stack is empty and should not be")
            raise
        if pop_tag != tag:
            raise ValueError("passed tag not top of stack")
        try:
            children_list = self.children_nodes.pop()
        except IndexError:
            print("children node stack is empty and should not be")
            raise
        node = ParentNode(pop_tag, children_list)
        if len(self.tag_stack):
            try:
                sibling_nodes = self.children_nodes.pop()
            except IndexError:
                print("children node stack is empty and should not be")
                raise
            sibling_nodes.append(node)
            self.children_nodes.append(sibling_nodes)
            return
        self.root_node = node

    def handle_data(self, data):
        node = LeafNode(None, data)
        if len(self.tag_stack):
            try:
                sibling_nodes = self.children_nodes.pop()
            except IndexError:
                print("children node stack is empty and should not be")
                raise
            sibling_nodes.append(node)
            self.children_nodes.append(sibling_nodes)
            return
        self.root_node = node

    def handle_startendtag(self, tag, attrs):
        return

    def handle_comment(self, data):
        return
