class HTMLNode():
    def __init__(self, tag=None, value=None, children=[]):
        self.tag = tag
        self.value = value
        self.children = children

    def __repr__(self):
        return (f"HTMLNode(tag='{self.tag}', value='{self.value}', "
                f"children={self.children})")

    def __eq__(self, o):
        if self.tag != o.tag:
            return False
        if self.value != o.value:
            return False
        if self.children != o.children:
            return False
        return True

    def __iter__(self):
        yield self
        for child in self.children:
            yield from child.__iter__()

    def __str__(self):
        child_count = len(self.children)
        return f"HTMLNode(tag='{self.tag}', value='{self.value}', children: {child_count})"


class ParentNode(HTMLNode):
    def __init__(self, tag, children):
        super().__init__(tag=tag, children=children)


class LeafNode(HTMLNode):
    def __init__(self, tag, value):
        super().__init__(tag=tag, value=value)
