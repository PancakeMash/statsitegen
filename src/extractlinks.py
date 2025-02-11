import re
from textnode import TextNode, TextType 

def extract_markdown_images(text):
    match = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return match

def extract_markdown_links(text):
    match = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)",text)
    return match


def split_nodes_link(old_nodes):
    node_list = []
    for old_node in old_nodes:
        # Skip non-normal nodes
        if old_node.text_type != TextType.NORMAL:
            node_list.append(old_node)
            continue

        match = extract_markdown_links(old_node.text)
        # If no matches found, preserve the original node
        if not match:
            node_list.append(old_node)
            continue
        
        copy_node = old_node.text
        
        for i in range(len(match)):
            image_alt = match[i][0]
            image_link = match[i][1]
            
            sections = copy_node.split(f"[{image_alt}]({image_link})",1) # split the first instance only
            before = sections[0]
            node_list.extend([TextNode(before,  TextType.NORMAL),
                            TextNode(image_alt, TextType.LINK, image_link)
                            ])
            
            if i == len(match) - 1:
                if 0 <= i+1 <= len(sections) and len(sections[1]) > 0:
                    (node_list.append(TextNode(sections[1], TextType.NORMAL)))
            if i != len(match) - 1:
                copy_node = sections[1]

    return node_list

def split_nodes_image(old_nodes):
    node_list = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.NORMAL:
            node_list.append(old_node)
            continue

        match = extract_markdown_images(old_node.text)
        if not match:
            # If no matches, preserve the original node
            node_list.append(old_node)
            continue
        
        copy_node = old_node.text

        for i in range(len(match)):
            image_alt = match[i][0]
            image_link = match[i][1]
            
            sections = copy_node.split(f"![{image_alt}]({image_link})",1) # split the first instance only
            before = sections[0]
            node_list.extend([TextNode(before,  TextType.NORMAL),
                            TextNode(image_alt, TextType.IMAGE, image_link)
                            ])
            
            if i == len(match) - 1:
                if 0 <= i+1 <= len(sections) and len(sections[1]) > 0:
                    (node_list.append(TextNode(sections[1], TextType.NORMAL)))
            if i != len(match) - 1:
                copy_node = sections[1]
    return node_list