from enum import Enum


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