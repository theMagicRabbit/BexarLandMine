import logging
from html.parser import HTMLParser
from BexarLandMine.HTML.Node import ParentNode, LeafNode
logger = logging.getLogger(__name__)


class BexarHTMLParser(HTMLParser):
    void_tags = [
        "area",
        "base",
        "br",
        "col",
        "embed",
        "hr",
        "img",
        "input",
        "link",
        "meta",
        "param",
        "source",
        "track",
        "wbr"
    ]
    broken_tags = [
            'b',  # acttax doesn't close bold tags
            'font',  # this is a deprecated void tag
    ]

    def __init__(self):
        self.tag_stack = []
        self.node_stack = []
        self.children_nodes = []
        self.root_node = None
        super().__init__()

    def __repr__(self):
        return "BexarHTMLParser()"

    def feed(self, data: str):
        cleaned = data.strip().replace('<br>', "\n").replace('<br/>', "\n")
        super().feed(cleaned)

    def handle_starttag(self, tag, attrs):
        if (tag in self.void_tags
                or tag in self.broken_tags):
            return
        logger.debug(f"starting tag: {tag}")
        self.tag_stack.append(tag)
        self.children_nodes.append([])

    def handle_endtag(self, tag):
        try:
            pop_tag = self.tag_stack.pop()
        except IndexError:
            print("tag stack is empty and should not be")
            raise
        if pop_tag != tag:
            logging.error(f"passed tag not top of stack: {tag}")
            logging.debug(f"stack top: {pop_tag}")
            self.tag_stack.append(pop_tag)
            return
        try:
            children_list = self.children_nodes.pop()
        except IndexError:
            logger.error("children node stack is empty and should not be")
            raise
        node = ParentNode(pop_tag, children_list)
        logger.debug(node)
        if len(self.tag_stack):
            try:
                sibling_nodes = self.children_nodes.pop()
            except IndexError:
                logger.error("children node stack is empty and should not be")
                raise
            sibling_nodes.append(node)
            self.children_nodes.append(sibling_nodes)
            logger.debug(self.children_nodes)
            return
        self.root_node = node

    def handle_startendtag(self, tag, attrs):
        return

    def handle_data(self, data):
        cleaned = data.strip()
        node = LeafNode(None, cleaned)
        if not cleaned:
            node = None
        if len(self.tag_stack) and node:
            try:
                sibling_nodes = self.children_nodes.pop()
            except IndexError:
                print("children node stack is empty and should not be")
                raise
            sibling_nodes.append(node)
            self.children_nodes.append(sibling_nodes)
            return
        self.root_node = node

    def handle_comment(self, data):
        return
