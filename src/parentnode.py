"""This module handles the nesting of HTML nodes (not LeafNodes) inside one another."""
from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        if not self.tag:
            raise ValueError

        if not self.children:
            raise ValueError("HTML children missing.")

        children_html: str = ""

        for child in self.children:
            children_html += child.to_html()

        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"

    def __repr__(self):
        return f"{self.__class__.__name__} tag=\"{self.tag}\", children=\"{self.children}\", props=\"{self.props}\""
