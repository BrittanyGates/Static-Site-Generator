import unittest
from leafnode import LeafNode
from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node: object = TextNode("This is a text node", TextType.BOLD_TEXT)
        node2: object = TextNode("This is a text node", TextType.BOLD_TEXT)
        self.assertEqual(node, node2)

    def test_not_equal_text_eq(self):
        node: object = TextNode("This is italic text", TextType.ITALIC_TEXT)
        node2: object = TextNode("This is code text", TextType.CODE_TEXT)
        self.assertNotEqual(node, node2)

    def test_url_eq(self):
        node: object = TextNode("This is plain text", TextType.PLAIN_TEXT, url=None)
        node2: object = TextNode("This is plain text", TextType.PLAIN_TEXT)
        self.assertEqual(node, node2)

    def test_not_equal_link_eq(self):
        node: object = TextNode("Text", TextType.LINK, "www.google.com")
        node2: object = TextNode("Text", TextType.LINK, "www.youtube.com")
        self.assertNotEqual(node, node2)

    def test_text(self):
        node: object = TextNode("This is a text node", TextType.PLAIN_TEXT)
        html_node: LeafNode = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_image(self):
        node: object = TextNode("Alt text", TextType.IMAGE, "https://path/to/image.jpg")
        html_node: LeafNode = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(html_node.props, {"src": "https://path/to/image.jpg", "alt": "Alt text"})

    def test_link(self):
        node: object = TextNode("Test link", TextType.LINK, "www.google.com")
        html_node: LeafNode = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "Test link")
        self.assertEqual(html_node.props, {"href": "www.google.com"})

    def test_invalid_text_type(self):
        node: object = TextNode("Text", "invalid_type")
        with self.assertRaisesRegex(ValueError, "Invalid text type:"):
            text_node_to_html_node(node)


if __name__ == "__main__":
    unittest.main()