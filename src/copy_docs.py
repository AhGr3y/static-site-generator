import os, shutil

def clear_dir(dir):

    # Check if dir exist
    if os.path.exists(dir) == True:
        # Remove dir
        shutil.rmtree(dir)
        # Create dir in same directory
        os.mkdir(dir)

def copy_docs(src, dst):
    
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
            # Recursively call copy_docs with doc as a new starting point directory
            copy_docs(src_path, dst_path)

        # Check if doc is a file
        elif os.path.isfile(src_path):
            # Copy doc to dst
            copy_path = shutil.copy(src_path, dst)
            # log the copy operation
            print(f'Copying "{src_path}" to "{copy_path}"')