import shutil
from textnode import TextNode, TextType
from markdowntohtml import *
from htmlnode import *
import os
import pathlib

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def print_directory_structure(startpath):
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * level
        print(f'{indent}{os.path.basename(root)}/')
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            print(f'{subindent}{f}')

print("\nProject structure:")
print_directory_structure(PROJECT_ROOT)

def copy_static(source_path, dest_path):
    print(f"Copying static files from {source_path} to {dest_path}")
    os.makedirs(dest_path, exist_ok=True)
    
    for item in os.listdir(source_path):
        source_item_path = os.path.join(source_path, item)
        dest_item_path = os.path.join(dest_path, item)
        
        print(f"Processing: {item}")
        print(f"From: {source_item_path}")
        print(f"To: {dest_item_path}")
        
        if os.path.isfile(source_item_path):
            print(f"Copying file: {item}")
            shutil.copy(source_item_path, dest_item_path)
        else:
            print(f"Copying directory: {item}")
            shutil.copytree(source_item_path, dest_item_path, dirs_exist_ok=True)

def extract_title(markdown):
    if len(markdown) == 0:
        raise Exception("markdown is empty")
    
    lines = markdown.split("\n")


    for line in lines:
        if line.startswith("# ") and line.count('#') == 1:
            return line[1:].strip()
        
    
    raise Exception("no header found")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    
    # Read the markdown file
    with open(from_path, 'r') as f:
        markdown_content = f.read()
    
    # Read the template file
    with open(template_path, 'r') as f:
        template_html = f.read()
    
    # Convert markdown to HTML and store it in html_node
    html_node = markdown_to_html_node(markdown_content)
    html_content = "".join(child.to_html() for child in html_node.children)
    
    # Get the title
    title = extract_title(markdown_content)
    
    # Replace the placeholders
    template_html = template_html.replace("{{ Title }}", title)
    template_html = template_html.replace("{{ Content }}", html_content)
    
    # Create directories if needed
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    
    # Write the final HTML
    with open(dest_path, 'w') as f:
        f.write(template_html)
    
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    print(f"\nStarting copy from {dir_path_content} to {dest_dir_path} using {template_path}")

    os.makedirs(dest_dir_path, exist_ok=True)

    for item in os.listdir(dir_path_content):
        source_item_path = os.path.join(dir_path_content, item)
        dest_item_path = os.path.join(dest_dir_path, item)

        if os.path.isfile(source_item_path):
            if source_item_path.endswith(".md"):
                dest_html_path = str(pathlib.Path(dest_item_path)).replace('.md', '.html')
                print(f"{source_item_path} is being converted to {dest_html_path}")
                generate_page(source_item_path, template_path, dest_html_path)
            else:
                # Handle non-markdown files (like images)
                print(f"{source_item_path} is being copied to {dest_item_path}")
                shutil.copy(source_item_path, dest_item_path)
        else:
            # Handle directories
            print(f"Creating directory: {dest_item_path}")
            os.makedirs(dest_item_path, exist_ok=True)
            generate_pages_recursive(source_item_path, template_path, dest_item_path)


def main():
    source = os.path.join(PROJECT_ROOT, "static")
    dest = os.path.join(PROJECT_ROOT, "public")
    print(f"PROJECT_ROOT: {PROJECT_ROOT}")
    print(f"Source path: {source}")
    print(f"Destination path: {dest}")
    print(f"Source exists: {os.path.exists(source)}")
    copy_static(source, dest)
    
    content_path = os.path.join(PROJECT_ROOT, "content")
    template_path = os.path.join(PROJECT_ROOT, "template.html")
    dest_path = os.path.join(PROJECT_ROOT, "public")
    
    generate_pages_recursive(content_path, template_path, dest_path)

    print("Static directory contents:", os.listdir("static"))
    print("Public directory contents:", os.listdir("public"))
   
if __name__ == "__main__":
    main()