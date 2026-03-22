import unittest
from leafnode import LeafNode
from parentnode import ParentNode


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node: LeafNode = LeafNode("span", "child")
        parent_node: ParentNode = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node: LeafNode = LeafNode("b", "grandchild")
        child_node: ParentNode = ParentNode("span", [grandchild_node])
        parent_node: ParentNode = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span><b>grandchild</b></span></div>")

    def test_empty_tag(self):
        parent_node: ParentNode = ParentNode(None, None)
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_empty_children(self):
        parent_node: ParentNode = ParentNode("div", None)
        with self.assertRaisesRegex(ValueError, "HTML children missing."):
            parent_node.to_html()

    def test_multiple_children(self):
        parent_node: ParentNode = ParentNode("div", [
            LeafNode("p", "child_node_one"),
            LeafNode("p", "child_node_two"),
            LeafNode("b", "child_node_three"),
            LeafNode("b", "child_node_four")
        ])
        self.assertEqual(parent_node.to_html(),
                         "<div><p>child_node_one</p><p>child_node_two</p><b>child_node_three</b><b>child_node_four</b></div>")

    def test_to_html_props(self):
        parent_node: ParentNode = ParentNode("div", [LeafNode("p", "child")], props={"class": "main", "id": "header"})
        self.assertEqual(parent_node.to_html(), "<div class=\"main\" id=\"header\"><p>child</p></div>")

    def test_to_html_with_multiple_grandchildren(self):
        parent_node: ParentNode = ParentNode("div", [
            ParentNode("div", [
                ParentNode("div", [
                    ParentNode("div", [LeafNode("p", "child")])
                ])
            ])
        ])
        self.assertEqual(parent_node.to_html(), "<div><div><div><div><p>child</p></div></div></div></div>")


if __name__ == "__main__":
    unittest.main()
