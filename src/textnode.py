from htmlnode import LeafNode

text_type_text = "text"
text_type_bold = "bold"
text_type_italic = "italic"
text_type_image = "image"
text_type_link = "link"
text_type_code = "code"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        return self.text == other.text and self.text_type == other.text_type and self.url == other.url

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"

    
def text_node_to_html_node(text_node):

    # Define valid text types
    valid_types = [
        text_type_text, 
        text_type_bold, 
        text_type_italic, 
        text_type_code, 
        text_type_link, 
        text_type_image
    ]

    # Raise an error if text type is invalid
    if text_node.text_type not in valid_types:
        raise ValueError(f"Invalid text type: {text_node.text_type}")

    # Return LeafNode for text type text
    if text_node.text_type == text_type_text:
        return LeafNode(None, text_node.text, None)

    # Return LeafNode for bold text
    if text_node.text_type == text_type_bold:
        return LeafNode("b", text_node.text, None)

    # Return LeafNode for italic text
    if text_node.text_type == text_type_italic:
        return LeafNode("i", text_node.text, None)

    # Return LeafNode for code text
    if text_node.text_type == text_type_code:
        return LeafNode("code", text_node.text, None)

    # Return LeafNode for link text
    if text_node.text_type == text_type_link:
        return LeafNode("a", text_node.text, {"href": text_node.url})

    # Return LeafNode for image text
    if text_node.text_type == text_type_image:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})

