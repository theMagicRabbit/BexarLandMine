class HTMLNode():
    def __init__(self, tag: str):
        self.tag = tag
        self.children = []

    def __repr__(self):
        return "HTMLNode()"
