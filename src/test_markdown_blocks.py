import unittest
from markdown_blocks import BlockType, block_to_block_type


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


if __name__ == "__main__":
    unittest.main()