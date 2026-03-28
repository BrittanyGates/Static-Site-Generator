"""This module contains the class to represent a node in an HTML document tree."""
class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if not self.props:
            return ""

        prop: str = ""

        for key, value in self.props.items():
            prop += f" {key}=\"{value}\""

        return prop

    def __repr__(self):
        return f"{self.__class__.__name__} tag=\"{self.tag}\", value=\"{self.value}\", children=\"{self.children}\", props=\"{self.props}\""
