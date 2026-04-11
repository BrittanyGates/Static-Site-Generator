"""This module contains the unit tests for the Markdown_blocks module."""
import unittest
from markdown_blocks import BlockType, block_to_block_type, markdown_to_html_node


class TestMarkdownBlocks(unittest.TestCase):
    def test_heading_block(self):
        block1 = "# Heading"
        block2 = "## Heading"
        block3 = "### Heading"
        block4 = "####### Heading"
        self.assertEqual(block_to_block_type(block1), BlockType.HEADING)
        self.assertEqual(block_to_block_type(block2), BlockType.HEADING)
        self.assertEqual(block_to_block_type(block3), BlockType.HEADING)
        self.assertEqual(block_to_block_type(block4), BlockType.PARAGRAPH)

    def test_code_block(self):
        block1 = "```\ncode\n```"
        block2 = "`Not code`"
        self.assertEqual(block_to_block_type(block1), BlockType.CODE)
        self.assertEqual(block_to_block_type(block2), BlockType.PARAGRAPH)

    def test_quote_block(self):
        block1 = ">Quote"
        block2 = "> Quote"
        block3 = "Not quote"
        block4 = "> Quote\nQuote"
        self.assertEqual(block_to_block_type(block1), BlockType.QUOTE)
        self.assertEqual(block_to_block_type(block2), BlockType.QUOTE)
        self.assertEqual(block_to_block_type(block3), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(block4), BlockType.PARAGRAPH)

    def test_unordered_list(self):
        block1 = "- List item"
        block2 = "-Not list item"
        self.assertEqual(block_to_block_type(block1), BlockType.UNORDERED_LIST)
        self.assertEqual(block_to_block_type(block2), BlockType.PARAGRAPH)

    def test_ordered_list(self):
        block1 = "1. List item\n2. List item"
        block2 = ". Not list item\n. Not list item"
        block3 = "1. List item\n3. List item"
        self.assertEqual(block_to_block_type(block1), BlockType.ORDERED_LIST)
        self.assertEqual(block_to_block_type(block2), BlockType.PARAGRAPH)
        self.assertEqual(block_to_block_type(block3), BlockType.PARAGRAPH)

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff</code></pre></div>",
        )


    def test_markdown_to_html_node_full(self):
        md = """
# Heading 1

This is a paragraph with **bold**, _italic_, and `code`.

> This is a multi-line
> quote block.

```
def hello():
    print("world")
```

- Item 1 with **bold**
- Item 2 with _italic_

1. First item
2. Second item"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertIn("<h1>Heading 1</h1>", html)
        self.assertIn("<b>bold</b>", html)
        self.assertIn("<i>italic</i>", html)
        self.assertIn("<blockquote>This is a multi-line quote block.</blockquote>", html)
        self.assertIn("<pre><code>def hello():\n    print(\"world\")</code></pre>", html)
        self.assertIn("<ul><li>Item 1 with <b>bold</b></li>", html)
        self.assertIn("<ol><li>First item</li><li>Second item</li></ol>", html)

if __name__ == "__main__":
    unittest.main()
