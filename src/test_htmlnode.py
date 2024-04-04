import unittest

from htmlnode import (
    HTMLNode,
    LeafNode,
    ParentNode,
)

class TestHTMLNode(unittest.TestCase):

    def test_eq(self):
        node = HTMLNode("p", "This is a test value")
        node2 = HTMLNode("p", "This is a test value")
        self.assertEqual(node, node2)

    def test_eq_false(self):
        node = HTMLNode("p", "This is a test value")
        node2 = HTMLNode("a", "This is a test value")
        self.assertNotEqual(node, node2)

    def test_eq_children(self):
        child = [HTMLNode()]
        child2 = [HTMLNode()]
        node = HTMLNode("a", "This is a test value", child)
        node2 = HTMLNode("a", "This is a test value", child2)
        self.assertEqual(node, node2)

    def test_eq_props(self):
        child = [HTMLNode()]
        child2 = [HTMLNode()]
        prop = {"href": "https://boot.dev", "target": "_blank"}
        prop2 = {"href": "https://boot.dev", "target": "_blank"}
        node = HTMLNode("a", "This is a test value", child, prop)
        node2 = HTMLNode("a", "This is a test value", child2, prop2)
        self.assertEqual(node, node2)
    
    def test_repr(self):
        child = [HTMLNode()]
        prop = {"href": "https://boot.dev", "target": "_blank"}
        node = HTMLNode("a", "This is a test value", child, prop)
        self.assertEqual("HTMLNode(a, This is a test value, children: [HTMLNode(None, None, children: None, None)], {'href': 'https://boot.dev', 'target': '_blank'})", repr(node))

    def test_props_to_html(self):
        props = {"href": "https://www.boot.dev", "target": "_blank"}
        node = HTMLNode(None, None, None, props)
        props_html = ' href="https://www.boot.dev" target="_blank"'
        self.assertEqual(props_html, node.props_to_html())

class TestLeafNode(unittest.TestCase):

    def test_eq(self):
        node = LeafNode("p", "This is a test value.", None)
        node2 = LeafNode("p", "This is a test value.", None)
        self.assertEqual(node, node2)

    def test_eq2(self):
        node = LeafNode(None, "This is a test value.", None)
        node2 = LeafNode(None, "This is a test value.", None)
        self.assertEqual(node, node2)

    def test_eq_false(self):
        node = LeafNode("p", "This is a test value.", None)
        node2 = LeafNode("a", "This is a test value.", None)
        self.assertNotEqual(node, node2)

    def test_to_html(self):
        node = LeafNode("a", "This is a test value.", {"href": "https://www.boot.dev", "test_key": "test_value"})
        self.assertEqual(node.to_html(), '<a href="https://www.boot.dev" test_key="test_value">This is a test value.</a>')

    def test_to_html_no_tag(self):
        node = LeafNode(None, "This is a test value.", None)
        self.assertEqual(node.to_html(), "This is a test value.")

class TestParentNode(unittest.TestCase):

    def test_to_html(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text", None),
                LeafNode(None, "Normal text", None),
                LeafNode("i", "italic text", None),
                LeafNode(None, "Normal text", None),
            ],
            None,
        )
        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

    def test_to_html2(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                ParentNode(
                    "p",
                    [
                        LeafNode("i", "italic text"),
                        LeafNode(None, "Normal text"),
                    ],
                    None,
                )
            ],
            None,
        )
        self.assertEqual(node.to_html(), "<p><b>Bold text</b><p><i>italic text</i>Normal text</p></p>")

    def test_to_html_with_grandchildren(self):
        grandchildren = LeafNode("p", "I am the grandchildren")
        parent = ParentNode("span", [grandchildren])
        grandparent = ParentNode("div", [parent])
        self.assertEqual(grandparent.to_html(), "<div><span><p>I am the grandchildren</p></span></div>")

if __name__ == "__main__":
    unittest.main()
