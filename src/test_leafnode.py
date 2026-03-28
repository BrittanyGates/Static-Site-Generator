"""This module contains the unit tests for the leafnode module."""
import unittest
from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node: LeafNode = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node: LeafNode = LeafNode("a", "Google", {"href": "www.google.com"})
        self.assertEqual(node.to_html(), '<a href="www.google.com">Google</a>')


if __name__ == "__main__":
    unittest.main()
