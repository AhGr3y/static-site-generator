from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node
from htmlnode import ParentNode

block_type_paragraph = "paragraph"
block_type_heading = "heading"
block_type_code = "code"
block_type_quote = "quote"
block_type_unordered_list = "unordered_list"
block_type_ordered_list = "ordered_list"

def markdown_to_blocks(markdown):
    blocks = []
    split_text = markdown.split("\n")
    block = ""
    
    for text in split_text:
        if text.strip() == "" and block != "":
            blocks.append(block.strip())
            block = ""
            continue
        if text.strip() == "":
            continue
        if text.strip() != "" and block != "":
            block += "\n" + text.strip()
            continue
        block += text
    if block.strip() != "":
        blocks.append(block.strip())
    return blocks

def block_to_block_type(block):
    lines = block.split("\n")

    if (
        block.startswith("# ") 
        or block.startswith("## ") 
        or block.startswith("### ") 
        or block.startswith("#### ") 
        or block.startswith("##### ") 
        or block.startswith("###### ")
    ):
        return block_type_heading

    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return block_type_paragraph
        return block_type_quote

    if block.startswith("```") and block.endswith("```") and len(lines) > 1:
        return block_type_code

    if block.startswith("* "):
        for line in lines:
            if not line.startswith("* "):
                return block_type_paragraph
        return block_type_unordered_list

    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return block_type_paragraph
        return block_type_unordered_list

    if block.startswith("1. "):
        for i in range(0, len(lines)):
            if not lines[i].startswith(f"{i+1}."):
                return block_type_paragraph
        return block_type_ordered_list
    
    return block_type_paragraph

def text_to_children(text):

    children = []

    # Split text into TextNodes
    text_nodes = text_to_textnodes(text)

    # Initialize HTMLNode for each TextNode and add into children
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node)
        children.append(html_node)

    return children

def quote_block_to_html_node(block):
    
    quote_lines = []
    
    # split quote block into lines
    lines = block.split("\n")

    for line in lines:

        # If line is invalid quote markdown, raise an error
        if not line.startswith(">"):
            raise ValueErro("Invalid quote markdown.")

        # remove '>' from quote markdown
        text = line[1:].strip()

        # Add text to quote_lines
        quote_lines.append(text)
    
    # Join quote_lines into a single string with whitespace in between
    quote_text = " ".join(quote_lines)

    # Convert quote_text to HTMLNode and append to children
    children = text_to_children(quote_text)

    return ParentNode("blockquote", children)

def unordered_list_block_to_html_node(block):

    children = []

    # Split block into lines
    lines = block.split("\n")

    for line in lines:
        li_children = []
        
        if line.startswith("- ") or line.startswith("* "): 

            # Remove leading "- " or "* "
            text = line[2:].strip()

            # convert text to HTMLNodes
            html_nodes = text_to_children(text)

            # For each HTMLNode, append to li_children
            for html_node in html_nodes:
                li_children.append(html_node)

            # Initialize HTMLNode for 'li' block
            li_node = ParentNode("li", li_children)

            # Add li_node to children
            children.append(li_node)
        
        else:
            # Raise an error for invalid unordered list syntax
            raise ValueError("Invalid unordered list markdown syntax.")
        

    return ParentNode("ul", children)

def ordered_list_block_to_html_node(block):

    ol_children = []
    list_num = 1

    # Split block into lines
    lines = block.split("\n")

    for line in lines:
        
        li_children = []

        # Get first character of line
        first_char = line[0]

        # Check for valid ordered list syntax
        if not line.startswith(f"{list_num}. "):
            raise ValueError("Invalid ordered list syntax.")

        # Remove leading prefix e.g. "1. " and whitespaces
        line = line[3:].strip()

        # Initialize HTMLNode with line
        html_nodes = text_to_children(line)

        # Add node to li_children
        for html_node in html_nodes:
            li_children.append(html_node)

        # Initialize HTMLNode for current line
        li_node = ParentNode("li", li_children)

        # Add li_node to ol_children
        ol_children.append(li_node)

        # Increment list_num by 1
        list_num += 1

    return ParentNode("ol", ol_children)

def code_block_to_html_node(block):
    
    # Check for valid code syntax
    if not block.startswith("```") or not block.endswith("```"):
        raise ValueError("Invalid code block")

    # Remove leading and trailing ``` from code block
    text = block[4:-4]

    # Convert text to HTMLNodes
    children = text_to_children(text)

    # Initialize "code" tag HTMLNode
    code = ParentNode("code", children)

    return ParentNode("pre", [code])

def heading_block_to_html_node(block):

    tag = ""
    valid = False

    # Set tag to appropriate value
    if block.startswith("# "):
        tag = "h1"
        valid = True
    if block.startswith("## "):
        tag = "h2"
        valid = True
    if block.startswith("### "):
        tag = "h3"
        valid = True
    if block.startswith("#### "):
        tag = "h4"
        valid = True
    if block.startswith("##### "):
        tag = "h5"
        valid = True
    if block.startswith("###### "):
        tag = "h6"
        valid = True

    # Check for valid headings markdown
    if not valid:
        raise ValueError("Invalid headings block")

    # Remove leading # and whitespace
    text = block.lstrip("# ").strip()

    # Convert text to list of LeafNode(s)
    children = text_to_children(text)

    return ParentNode(tag, children)

def paragraph_block_to_html_node(block):
    
    # Split block into lines
    lines = block.split("\n")

    # Join lines into a single string
    text = " ".join(lines)

    # Convert text to list of LeafNode(s)
    children = text_to_children(text)

    return ParentNode("p", children)

def markdown_to_html_node(md):

    children = []

    # Convert markdown to blocks
    blocks = markdown_to_blocks(md)

    # Loop through blocks
    for block in blocks:

        # Convert block to html node and add to children
        node = block_to_html_node(block)
        children.append(node)

    return ParentNode("div", children)

def block_to_html_node(block):
    
    # Check for block type
    block_type = block_to_block_type(block)

    # Convert paragraph block to html node and return it
    if block_type == block_type_paragraph:
        return paragraph_block_to_html_node(block)

    # Convert heading block to html node and return it
    if block_type == block_type_heading:
        return heading_block_to_html_node(block)

    # Convert code block to html node and return it
    if block_type == block_type_code:
        return code_block_to_html_node(block)

    # Convert quote block to html node and return it
    if block_type == block_type_quote:
        return quote_block_to_html_node(block)

    # Convert unordered list block to html node and return it
    if block_type == block_type_unordered_list:
        return unordered_list_block_to_html_node(block)

    # Convert ordered list block to html node and return it
    if block_type == block_type_ordered_list:
        return ordered_list_block_to_html_node(block)

    # Raise error for invalid block
    raise ValueError("Invalid block type")