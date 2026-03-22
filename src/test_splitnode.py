import unittest
from splitnode import split_nodes_delimiter, extract_markdown_images, extract_markdown_links
from textnode import TextNode, TextType


class TestSplitNode(unittest.TestCase):
    def test_no_delimiter(self):
        node: object = TextNode("This is plain text", TextType.PLAIN_TEXT)
        self.assertEqual(split_nodes_delimiter([node], "`", node.text_type),
                         [node])

    def test_code_block(self):
        node: object = TextNode("This is `code` block", TextType.PLAIN_TEXT)
        new_nodes: list = split_nodes_delimiter([node], "`", TextType.CODE_TEXT)
        self.assertEqual(new_nodes, [
            TextNode("This is ", TextType.PLAIN_TEXT),
            TextNode("code", TextType.CODE_TEXT),
            TextNode(" block", TextType.PLAIN_TEXT)
        ])

    def test_bold_text(self):
        node: object = TextNode("This is **bold** text", TextType.PLAIN_TEXT)
        new_nodes: list = split_nodes_delimiter([node], "**", TextType.BOLD_TEXT)
        self.assertEqual(new_nodes, [
            TextNode("This is ", TextType.PLAIN_TEXT),
            TextNode("bold", TextType.BOLD_TEXT),
            TextNode(" text", TextType.PLAIN_TEXT)
        ])

    def test_italic_text(self):
        node: object = TextNode("This is *italic* text", TextType.PLAIN_TEXT)
        new_nodes: list = split_nodes_delimiter([node], "*", TextType.ITALIC_TEXT)
        self.assertEqual(new_nodes, [
            TextNode("This is ", TextType.PLAIN_TEXT),
            TextNode("italic", TextType.ITALIC_TEXT),
            TextNode(" text", TextType.PLAIN_TEXT)
        ])

    def test_multiple_nodes(self):
        node1: object = TextNode("This is `code` block", TextType.PLAIN_TEXT)
        node2: object = TextNode("No delimiters here", TextType.PLAIN_TEXT)
        new_nodes: list = split_nodes_delimiter([node1, node2], "`", TextType.CODE_TEXT)
        self.assertEqual(new_nodes, [
            TextNode("This is ", TextType.PLAIN_TEXT),
            TextNode("code", TextType.CODE_TEXT),
            TextNode(" block", TextType.PLAIN_TEXT),
            TextNode("No delimiters here", TextType.PLAIN_TEXT)
        ])

    def test_missing_delimiter(self):
        node: object = TextNode("This is *italic text", TextType.PLAIN_TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "*", TextType.ITALIC_TEXT)

    def test_extract_markdown_images(self):
        matches: list = extract_markdown_images("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)")
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches: list = extract_markdown_links("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)")
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)


if __name__ == "__main__":
    unittest.main()
