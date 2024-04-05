import os, shutil

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

from copy_docs import (
    clear_dir,
    copy_docs,
)

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

def main():
    pass

main()

if __name__ == "__main__":

    from_path = "./content/index.md"
    template_path = "./template.html"
    dest_path = "./public/index.html"
    generate_page(from_path, template_path, dest_path)
    