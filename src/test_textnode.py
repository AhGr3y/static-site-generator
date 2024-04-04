import unittest

from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_link,
    text_type_image,
)

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "bold")
        self.assertEqual(node, node2)

    def test_eq_false(self):
        node = TextNode("This is a text node", "bold")
        node2 = TextNode("This is a text node", "italic")
        self.assertNotEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("This is a text node", "code", "https://www.boot.dev")
        node2 = TextNode("This is really a text node", "image", "https://www.boot.dev")
        self.assertEqual(node.url, node2.url)

    def test_repr(self):
        node = TextNode("This is really really a text node", "text")
        self.assertEqual("TextNode(This is really really a text node, text, None)", repr(node))

if __name__ == "__main__":
    unittest.main()
