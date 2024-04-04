import unittest

from block_markdown import (
    markdown_to_blocks,
    block_to_block_type,
    block_type_paragraph,
    block_type_heading,
    block_type_code,
    block_type_quote,
    block_type_unordered_list,
    block_type_ordered_list,
    quote_block_to_html_node,
    unordered_list_block_to_html_node,
    ordered_list_block_to_html_node,
    code_block_to_html_node,
    heading_block_to_html_node,
    paragraph_block_to_html_node,
    markdown_to_html_node,
)

from htmlnode import (
    HTMLNode,
    LeafNode,
    ParentNode,
)

class TestBlockMarkdown(unittest.TestCase):

    def test_markdown_to_blocks(self):
        markdown = """This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items"""
        result = [
            "This is **bolded** paragraph",
            "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
            "* This is a list\n* with items",
        ]
        self.assertListEqual(result, markdown_to_blocks(markdown))

    def test_markdown_to_blocks_newlines(self):
        markdown = """This is **bolded** paragraph




This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items"""
        result = [
            "This is **bolded** paragraph",
            "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
            "* This is a list\n* with items",
        ]
        self.assertListEqual(result, markdown_to_blocks(markdown))

    def test_block_to_block_type_paragraph(self):
        block = "I am a paragraph"
        result = block_type_paragraph
        self.assertEqual(result, block_to_block_type(block))

    def test_block_to_block_type_heading1(self):
        block = "# I am a heading 1"
        result = block_type_heading
        self.assertEqual(result, block_to_block_type(block))

    def test_block_to_block_type_heading2(self):
        block = "## I am a heading 2"
        result = block_type_heading
        self.assertEqual(result, block_to_block_type(block))

    def test_block_to_block_type_code(self):
        block = "```\nI am a code block\n```"
        result = block_type_code
        self.assertEqual(result, block_to_block_type(block))

    def test_block_to_block_type_quote(self):
        block = "> I am a quote.\n> I am another quote."
        result = block_type_quote
        self.assertEqual(result, block_to_block_type(block))

    def test_block_to_block_type_unordered_list1(self):
        block = "* I am an unordered list\n* I am another unordered list"
        result = block_type_unordered_list
        self.assertEqual(result, block_to_block_type(block))

    def test_block_to_block_type_unordered_list2(self):
        block = "- I am an unordered list\n- I am another unordered list"
        result = block_type_unordered_list
        self.assertEqual(result, block_to_block_type(block))

    def test_block_to_block_type_ordered_list(self):
        block = "1. I am an ordered list\n2. I am an ordered list"
        result = block_type_ordered_list
        self.assertEqual(result, block_to_block_type(block))

    def test_quote_block_to_html_node(self):
        block = ">Some text.\n>Some other text."
        result = quote_block_to_html_node(block)
        children = [
            LeafNode(None, "Some text. Some other text."),
        ]
        self.assertEqual(result, ParentNode("blockquote", children))

    def test_unordered_list_block_to_html_node(self):
        block = "- Some text\n* Some other text"
        children = [
            ParentNode("li", [LeafNode(None, "Some text")]),
            ParentNode("li", [LeafNode(None, "Some other text")])
        ]
        result = unordered_list_block_to_html_node(block)
        self.assertEqual(result, ParentNode("ul", children))

    def test_ordered_list_block_to_html_node(self):
        block = "1. First item\n2. Second item"
        children = [
            ParentNode("li", [LeafNode(None, "First item")]),
            ParentNode("li", [LeafNode(None, "Second item")]),
        ]
        result = ordered_list_block_to_html_node(block)
        self.assertEqual(result, ParentNode("ol", children))

    def test_code_block_to_html_node(self):
        block = "```\nI am in a code block\n```"
        result = code_block_to_html_node(block)
        code_children = [
            LeafNode(None, "I am in a code block"), 
        ]
        pre_children = [
            ParentNode("code", code_children)
        ]
        self.assertEqual(result, ParentNode("pre", pre_children))

    def test_heading_block_to_html_node_h1(self):
        block = "# Headings"
        result = heading_block_to_html_node(block)
        children = [
            LeafNode(None, "Headings")
        ]
        self.assertEqual(result, ParentNode("h1", children))

    def test_heading_block_to_html_node_h2(self):
        block = "## Headings"
        result = heading_block_to_html_node(block)
        children = [
            LeafNode(None, "Headings")
        ]
        self.assertEqual(result, ParentNode("h2", children))

    def test_paragraph_block_to_html_node(self):
        block = "Some text\nSome other text"
        result = paragraph_block_to_html_node(block)
        children = [
            LeafNode(None, "Some text Some other text")
        ]
        self.assertEqual(result, ParentNode("p", children))

    def test_markdown_to_html_node1(self):
        md = """
>Quote text
>Quote text 2

1. Ordered text
2. Ordered text 2
"""     
        result = markdown_to_html_node(md)
        blockquote_children = [
            LeafNode(None, "Quote text Quote text 2")
        ]
        li1_children = [
            LeafNode(None, "Ordered text")
        ]
        li2_children = [
            LeafNode(None, "Ordered text 2")
        ]
        ol_children = [
            ParentNode("li", li1_children),
            ParentNode("li", li2_children),
        ]
        children = [
            ParentNode("blockquote", blockquote_children),
            ParentNode("ol", ol_children)
        ]
        self.assertEqual(result, ParentNode("div", children))

    def test_paragraph(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with *italic* text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_lists(self):
        md = """
- This is a list
- with items
- and *more* items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )

if __name__ == "__main__":
    unittest.main()