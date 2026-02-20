import unittest
from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD_TEXT)
        self.assertEqual(node, node2)

    def test_not_equal_text_eq(self):
        node = TextNode("This is italic text", TextType.ITALIC_TEXT)
        node2 = TextNode("This is code text", TextType.CODE_TEXT)
        self.assertNotEqual(node, node2)

    def test_url_eq(self):
        node = TextNode("This is plain text", TextType.PLAIN_TEXT, url=None)
        node2 = TextNode("This is plain text", TextType.PLAIN_TEXT)
        self.assertEqual(node, node2)

    def test_not_equal_link_eq(self):
        node = TextNode("Text", TextType.LINK, "www.google.com")
        node2 = TextNode("Text", TextType.LINK, "www.youtube.com")
        self.assertNotEqual(node, node2)


if __name__ == "__main__":
    unittest.main()