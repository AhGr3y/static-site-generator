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

def clear_dir(dir):

    # Check if dir exist
    if os.path.exists(dir) == True:
        # Remove dir
        shutil.rmtree(dir)
        # Create dir in same directory
        os.mkdir(dir)

def copy_static_to_public(src, dst):
    
    # Raise error if src does not exist
    if os.path.exists(src) == False:
        raise ValueError("src does not exist!")

    # If dst does not exist, create it
    if os.path.exists(dst) == False:
        os.mkdir(dst)

    # Split files/directories in src into a list
    docs = os.listdir(src)

    # Loop through docs
    for doc in docs:

        # Get path for doc on src and dst
        src_path = os.path.join(src, f"{doc}")
        dst_path = os.path.join(dst, f"{doc}")

        # Check if doc is a directory
        if os.path.isfile(src_path) == False:
            # Create a directory with same name as doc on dst
            os.mkdir(dst_path)
            # Recursively call copy_static_to_public with doc as a new starting point directory
            copy_static_to_public(src_path, dst_path)

        # Check if doc is a file
        elif os.path.isfile(src_path):
            # Copy doc to dst
            copy_path = shutil.copy(src_path, dst)
            # log the copy operation
            print(f'Copying "{src_path}" to "{copy_path}"')

def main():
    pass

main()

if __name__ == "__main__":
    """
    staticDir = "./static"
    publicDir = "./public"
    clear_dir(publicDir)
    copy_static_to_public(staticDir, publicDir)
    """

    from_path = "./content/index.md"
    template_path = "./template.html"
    dest_path = "./public/index.html"
    generate_page(from_path, template_path, dest_path)
    