import re

from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link,
)

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        split_text = old_node.text.split(delimiter)
        if len(split_text) % 2 == 0:
            raise ValueError("Invalid markdown syntax")
        for i in range(len(split_text)):
            if split_text[i] == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(split_text[i], text_type_text))
            else:
                new_nodes.append(TextNode(split_text[i], text_type))
    return new_nodes

def extract_markdown_images(text):
    return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

def extract_markdown_links(text):
    return re.findall(r"\[(.*?)\]\((.*?)\)", text)

def split_nodes_image(old_nodes):
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        images = extract_markdown_images(old_node.text)
        if len(images) == 0:
            new_nodes.append(old_node)
            continue
        current_text = old_node.text
        for image in images:
            split_text = current_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(split_text) != 2:
                raise ValueError("Invalid markdown syntax for image")
            else:
                if split_text[0]:
                    new_nodes.append(TextNode(split_text[0], text_type_text))
                new_nodes.append(TextNode(image[0], text_type_image, image[1]))
                current_text = split_text[1]
        if current_text:
            new_nodes.append(TextNode(current_text, text_type_text))
    
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []

    for old_node in old_nodes:
        if old_node.text_type != text_type_text:
            new_nodes.append(old_node)
            continue
        links = extract_markdown_links(old_node.text)
        if len(links) == 0:
            new_nodes.append(old_node)
            continue
        current_text = old_node.text
        for link in links:
            split_text = current_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(split_text) != 2:
                raise ValueError("Invalid markdown syntax for link")
            else:
                if split_text[0]:
                    new_nodes.append(TextNode(split_text[0], text_type_text))
                new_nodes.append(TextNode(link[0], text_type_link, link[1]))
                current_text = split_text[1]
        if current_text:
            new_nodes.append(TextNode(current_text, text_type_text))
    
    return new_nodes

def text_to_textnodes(text):

    # Initialize a TextNode from input text
    text_node = TextNode(text, text_type_text)

    # Split bold text into TextNodes
    split_by_bold = split_nodes_delimiter([text_node], "**", text_type_bold)
    
    # Split italic text into TextNodes
    split_by_italic = split_nodes_delimiter(split_by_bold, "*", text_type_italic)
    
    # Split code text into TextNodes
    split_by_code = split_nodes_delimiter(split_by_italic, "`", text_type_code)
    
    # Split image text into TextNodes
    split_by_image = split_nodes_image(split_by_code)

    # Split link text into TextNodes
    split_by_link = split_nodes_link(split_by_image)
    
    return split_by_link