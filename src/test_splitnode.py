import unittest
from splitnode import split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, \
    split_nodes_link
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
        matches: list = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)")
        self.assertListEqual(
            [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.PLAIN_TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.PLAIN_TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.PLAIN_TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images_at_beginning(self):
        node = TextNode("![image](https://link/to/image.jpg) text after the image", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([
            TextNode("image", TextType.IMAGE, "https://link/to/image.jpg"),
            TextNode(" text after the image", TextType.PLAIN_TEXT),
        ],
            new_nodes,
        )

    def test_split_images_at_end(self):
        node = TextNode("Text before the image ![image](https://link/to/image.jpg)", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([
            TextNode("Text before the image ", TextType.PLAIN_TEXT),
            TextNode("image", TextType.IMAGE, "https://link/to/image.jpg"),
        ],
            new_nodes,
        )

    def test_no_images(self):
        node = TextNode("There's no image", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([
            TextNode("There's no image", TextType.PLAIN_TEXT),
        ],
            new_nodes,
        )

    def test_identical_images(self):
        node = TextNode(
            "Image one: ![image](https://link/to/image.jpg). Image two: ![image](https://link/to/image.jpg)",
            TextType.PLAIN_TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([
            TextNode("Image one: ", TextType.PLAIN_TEXT),
            TextNode("image", TextType.IMAGE, "https://link/to/image.jpg"),
            TextNode(". Image two: ", TextType.PLAIN_TEXT),
            TextNode("image", TextType.IMAGE, "https://link/to/image.jpg"),
        ],
            new_nodes,
        )

    def test_no_links(self):
        node = TextNode("There's no link", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([
            TextNode("There's no link", TextType.PLAIN_TEXT),
        ],
            new_nodes,
        )

    def test_split_link_at_beginning(self):
        node = TextNode("[link](https://www.google.com) text after the link", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([
            TextNode("link", TextType.LINK, "https://www.google.com"),
            TextNode(" text after the link", TextType.PLAIN_TEXT),
        ],
            new_nodes,
        )

    def test_identical_links(self):
        node = TextNode(
            "Link one: [link](https://www.youtube.com). Link two: [link](https://www.youtube.com)",
            TextType.PLAIN_TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual([
            TextNode("Link one: ", TextType.PLAIN_TEXT),
            TextNode("link", TextType.LINK, "https://www.youtube.com"),
            TextNode(". Link two: ", TextType.PLAIN_TEXT),
            TextNode("link", TextType.LINK, "https://www.youtube.com"),
        ],
            new_nodes,
        )

    def test_mixed_nodes(self):
        nodes = [
            TextNode("This is bold text.", TextType.BOLD_TEXT),
            TextNode("This is a link: [link](https://www.google.com)", TextType.PLAIN_TEXT),
        ]
        new_nodes = split_nodes_link(nodes)
        self.assertListEqual([
            TextNode("This is bold text.", TextType.BOLD_TEXT, None),
            TextNode("This is a link: ", TextType.PLAIN_TEXT),
            TextNode("link", TextType.LINK, "https://www.google.com"),
        ],
            new_nodes,
        )

    def test_just_markdown(self):
        node = TextNode("![img](https://.url)", TextType.PLAIN_TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual([
            TextNode("img", TextType.IMAGE, "https://.url")
        ],
            new_nodes,
        )


if __name__ == "__main__":
    unittest.main()
