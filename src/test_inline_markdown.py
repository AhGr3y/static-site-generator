import unittest

from inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)

from htmlnode import HTMLNode

from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link,
)

class TestInlineMarkdown(unittest.TestCase):

    def test_split_nodes_delimiter_bold(self):
            old_nodes = [
                TextNode("This is a **bold** text", text_type_text),
            ]
            delimiter = "**"
            text_type = text_type_bold
            result = [
                TextNode("This is a ", text_type_text),
                TextNode("bold", text_type_bold),
                TextNode(" text", text_type_text),
            ]
            self.assertListEqual(result, split_nodes_delimiter(old_nodes, delimiter, text_type))

    def test_split_nodes_delimiter_with_multiple_bold_text(self):
        old_nodes = [
            TextNode("Boots is a **great wizard** and also a **terrific teacher**!", text_type_text),
        ]
        delimiter = "**"
        text_type = text_type_bold
        result = [
            TextNode("Boots is a ", text_type_text),
            TextNode("great wizard", text_type_bold),
            TextNode(" and also a ", text_type_text),
            TextNode("terrific teacher", text_type_bold),
            TextNode("!", text_type_text),
        ]
        self.assertListEqual(result, split_nodes_delimiter(old_nodes, delimiter, text_type))
    
    def test_split_nodes_delimiter_italic(self):
            old_nodes = [
                TextNode("This is a *italic* text", text_type_text),
            ]
            delimiter = "*"
            text_type = text_type_italic
            result = [
                TextNode("This is a ", text_type_text),
                TextNode("italic", text_type_italic),
                TextNode(" text", text_type_text),
            ]
            self.assertListEqual(result, split_nodes_delimiter(old_nodes, delimiter, text_type))
    
    def test_split_nodes_delimiter_code(self):
            old_nodes = [
                TextNode("This is a `code` text", text_type_text),
            ]
            delimiter = "`"
            text_type = text_type_code
            result = [
                TextNode("This is a ", text_type_text),
                TextNode("code", text_type_code),
                TextNode(" text", text_type_text),
            ]
            self.assertListEqual(result, split_nodes_delimiter(old_nodes, delimiter, text_type))

    def test_extract_image(self):
        text = "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and ![another](https://i.imgur.com/dfsdkjfd.png)"
        output = [("image", "https://i.imgur.com/zjjcJKZ.png"), ("another", "https://i.imgur.com/dfsdkjfd.png")]
        self.assertListEqual(output, extract_markdown_images(text))

    def test_extract_link(self):
        text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
        output = [("link", "https://www.example.com"), ("another", "https://www.example.com/another")]
        self.assertListEqual(output, extract_markdown_links(text))

    def test_split_image(self):
        node = TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)", text_type_text)
        old_nodes = [node]
        result = [
            TextNode("This is text with an ", text_type_text),
            TextNode("image", text_type_image, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", text_type_text),
            TextNode("second image", text_type_image, "https://i.imgur.com/3elNhQu.png"),
        ]
        self.assertListEqual(result, split_nodes_image(old_nodes))

    def test_split_multiple_image(self):
        node = TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)", text_type_text)
        node2 = TextNode("First image: ![image](https://i.imgur.com/zjjcJKZ.png). Second image: ![second image](https://i.imgur.com/3elNhQu.png).", text_type_text)
        old_nodes = [node, node2]
        result = [
            TextNode("This is text with an ", text_type_text),
            TextNode("image", text_type_image, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and another ", text_type_text),
            TextNode("second image", text_type_image, "https://i.imgur.com/3elNhQu.png"),
            TextNode("First image: ", text_type_text),
            TextNode("image", text_type_image, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(". Second image: ", text_type_text),
            TextNode("second image", text_type_image, "https://i.imgur.com/3elNhQu.png"),
            TextNode(".", text_type_text),
        ]
        self.assertListEqual(result, split_nodes_image(old_nodes))

    def test_split_image_without_image_and_empty_string(self):
        node = TextNode("This is text without an image", text_type_text)
        node2 = TextNode("", text_type_text)
        old_nodes = [node, node2]
        result = [
            TextNode("This is text without an image", text_type_text),
            TextNode("", text_type_text),
        ]
        self.assertListEqual(result, split_nodes_image(old_nodes))

    def test_split_link(self):
        node = TextNode("This is text with an [link](https://www.boot.dev) and another [second link](https://www.boot.dev)", text_type_text)
        old_nodes = [node]
        result = [
            TextNode("This is text with an ", text_type_text),
            TextNode("link", text_type_link, "https://www.boot.dev"),
            TextNode(" and another ", text_type_text),
            TextNode("second link", text_type_link, "https://www.boot.dev"),
        ]
        self.assertListEqual(result, split_nodes_link(old_nodes))

    def test_split_side_by_side_link(self):
        node = TextNode("Testing [link](https://www.boot.dev)[second link](https://www.boot.dev)", text_type_text)
        old_nodes = [node]
        result = [
            TextNode("Testing ", text_type_text),
            TextNode("link", text_type_link, "https://www.boot.dev"),
            TextNode("second link", text_type_link, "https://www.boot.dev"),
        ]
        self.assertListEqual(result, split_nodes_link(old_nodes))

    def test_text_to_textnodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)"
        result = [
            TextNode("This is ", text_type_text),
            TextNode("text", text_type_bold),
            TextNode(" with an ", text_type_text),
            TextNode("italic", text_type_italic),
            TextNode(" word and a ", text_type_text),
            TextNode("code block", text_type_code),
            TextNode(" and an ", text_type_text),
            TextNode("image", text_type_image, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and a ", text_type_text),
            TextNode("link", text_type_link, "https://boot.dev"),
        ]
        self.assertListEqual(result, text_to_textnodes(text))

    def test_text_to_textnodes_jumbled_up_types(self):
        text = "This is **text** with an *italic* word and an ![image](https://i.imgur.com/zjjcJKZ.png) and **another bold text** and another ![second image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)"
        result = [
            TextNode("This is ", text_type_text),
            TextNode("text", text_type_bold),
            TextNode(" with an ", text_type_text),
            TextNode("italic", text_type_italic),
            TextNode(" word and an ", text_type_text),
            TextNode("image", text_type_image, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and ", text_type_text),
            TextNode("another bold text", text_type_bold),
            TextNode(" and another ", text_type_text),
            TextNode("second image", text_type_image, "https://i.imgur.com/zjjcJKZ.png"),
            TextNode(" and a ", text_type_text),
            TextNode("link", text_type_link, "https://boot.dev"),
        ]
        self.assertListEqual(result, text_to_textnodes(text))

if __name__ == "__main__":
    unittest.main()