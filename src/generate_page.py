import os

from pathlib import Path

from htmlnode import (
    HTMLNode,
    ParentNode,
    LeafNode,
)

from block_markdown import (
    markdown_to_html_node,
    markdown_to_blocks,
    block_to_block_type,
    block_type_heading,
)

def extract_title(md):

    # If md is empty, return empty string
    if len(md) == 0:
        return ""

    # Convert md to markdown blocks
    blocks = markdown_to_blocks(md)

    # Loop through blocks
    for block in blocks:
        # Get block type
        block_type = block_to_block_type(block)
        # Check if block type is heading
        if block_type == block_type_heading:
            # Check if its h1 heading
            if block.startswith("# "):
                # Extract text from block and return it
                return block[2:]
    
    # Raise error as no h1 found
    raise ValueError("Invalid markdown for html")

def generate_page(from_path, template_path, dest_path):
    
    # Print what this function is about to do
    print(f'Generating page from "{from_path}" to "{dest_path}" using "{template_path}"')

    # Check if from_path exist
    if os.path.exists(from_path):
        # Open file at from_path
        file = open(from_path, "r")
        # Store contents of from_path
        md = file.read()
        # Convert the contents to HTML
        html = markdown_to_html_node(md).to_html()
        # Get title of content
        title = extract_title(md)
        # Close the file at from_path
        file.close()
    else:
        # Raise error if from_path does not exist
        raise ValueError(f'"{from_path}" does not exist!')

    # Check if template_path exist
    if os.path.exists(template_path):
        # Open file at template_path
        file = open(template_path, "r")
        # Store contents of template_path
        template = file.read()
        # Replace title and contents of the template
        new_html = template.replace("{{ Title }}", title)
        new_html = new_html.replace("{{ Content }}", html)
        # Close the file at template_path
        file.close()

    # If directory of dest_path don't exist
    if not os.path.exists(os.path.dirname(dest_path)):
        # Create directory of dest_path
        os.makedirs(os.path.dirname(dest_path))

    # Create dest_path
    with open(dest_path, "w") as f:
        # Write content of new_html to dest_path
        f.write(new_html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    
    # If dir_path_content does not exist, raise an error
    if os.path.exists(dir_path_content) == False:
        raise ValueError("dir_path_content does not exist!")

    # List items in dir_path_content
    docs = os.listdir(dir_path_content)

    # Loop through docs
    for doc in docs:
        # Get doc path
        doc_path = os.path.join(dir_path_content, doc)
        # Check if doc is a file
        if os.path.isfile(doc_path):
            # Create Path object with doc
            doc_path_obj = Path(doc_path)
            # Get doc suffix
            doc_suffix = doc_path_obj.suffix
            # Check if doc is a markdown file
            if doc_suffix == ".md":
                # Get path of doc in dest_dir_path
                doc_dest_path = os.path.join(dest_dir_path, "index.html")
                # Generate a .html file using doc_dest_path and store it in dest_dir_path
                generate_page(doc_path, template_path, doc_dest_path)
        
        # Check if doc is a directory
        if os.path.isdir(doc_path):
            # Get path of doc in dest_dir_path
            doc_dest_path = os.path.join(dest_dir_path, doc)
            # Recursively call generate_pages_recursive
            generate_pages_recursive(doc_path, template_path, doc_dest_path)