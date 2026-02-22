import unittest
from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_htmlnode_empty_props(self):
        self.assertEqual(HTMLNode(props=None).props_to_html(), "")

    def test_htmlnode_nonempty_props(self):
        node = HTMLNode(props={"href": "www.google.com"})
        self.assertEqual(node.props_to_html(), ' href="www.google.com"')

    def test_htmlnode_multi_props(self):
        node = HTMLNode(props={"p": "This is text", "href": "This is a link"})
        self.assertEqual(node.props_to_html(), ' p="This is text" href="This is a link"')

if __name__ == "__main__":
    unittest.main()
