from enum import Enum
from leafnode import LeafNode


class TextType(Enum):
    PLAIN_TEXT = "text"
    BOLD_TEXT = "bold"
    ITALIC_TEXT = "italic"
    CODE_TEXT = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if (self.text, self.text_type, self.url) == (other.text, other.text_type, other.url):
            return True
        return False

    def __repr__(self):
        return f"{self.__class__.__name__}({self.text}, {self.text_type.value}, {self.url})"


def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.PLAIN_TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD_TEXT:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC_TEXT:
            return LeafNode("i", text_node.text)
        case TextType.CODE_TEXT:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", f"{text_node.text}", {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    return ValueError(f"Invalid text type: {text_node.text_type}")
