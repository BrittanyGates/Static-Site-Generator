import unittest
from splitnode import split_nodes_delimiter
from textnode import TextNode, TextType


class TestSplitNode(unittest.TestCase):
    def test_no_delimiter(self):
        node = TextNode("This is plain text", TextType.PLAIN_TEXT)
        self.assertEqual(split_nodes_delimiter([node], "`", node.text_type),
                         [node])

    def test_code_block(self):
        node = TextNode("This is `code` block", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE_TEXT)
        self.assertEqual(new_nodes, [
            TextNode("This is ", TextType.PLAIN_TEXT),
            TextNode("code", TextType.CODE_TEXT),
            TextNode(" block", TextType.PLAIN_TEXT)
        ])

    def test_bold_text(self):
        node = TextNode("This is **bold** text", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD_TEXT)
        self.assertEqual(new_nodes, [
            TextNode("This is ", TextType.PLAIN_TEXT),
            TextNode("bold", TextType.BOLD_TEXT),
            TextNode(" text", TextType.PLAIN_TEXT)
        ])

    def test_italic_text(self):
        node = TextNode("This is *italic* text", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC_TEXT)
        self.assertEqual(new_nodes, [
            TextNode("This is ", TextType.PLAIN_TEXT),
            TextNode("italic", TextType.ITALIC_TEXT),
            TextNode(" text", TextType.PLAIN_TEXT)
        ])

    def test_multiple_nodes(self):
        node1 = TextNode("This is `code` block", TextType.PLAIN_TEXT)
        node2 = TextNode("No delimiters here", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_delimiter([node1, node2], "`", TextType.CODE_TEXT)
        self.assertEqual(new_nodes, [
            TextNode("This is ", TextType.PLAIN_TEXT),
            TextNode("code", TextType.CODE_TEXT),
            TextNode(" block", TextType.PLAIN_TEXT),
            TextNode("No delimiters here", TextType.PLAIN_TEXT)
        ])

    def test_missing_delimiter(self):
        node = TextNode("This is *italic text", TextType.PLAIN_TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "*", TextType.ITALIC_TEXT)


if __name__ == "__main__":
    unittest.main()