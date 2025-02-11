from htmlnode import HTMLNode
from textnode import TextNode, TextType
from splitblocks import *
from texthtmlconvert import *

def find_next_delimiter(text):
    delimiters = ["**", "*", "`"]

    
    first_positions = []
    for delimiter in delimiters:
        pos = text.find(delimiter)

        if pos != -1:
            first_positions.append((pos, delimiter))
    
    if not first_positions:
        return -1
    
    sort_pos = sorted(first_positions, key=lambda x: x[0])
    return sort_pos[0]

def find_next_link(text):
    open_bracket = text.find("[")
    if open_bracket == -1:
        return -1
    
    is_image = open_bracket > 0 and text[open_bracket - 1] == "!"
    start_index = open_bracket - 1 if is_image else open_bracket
    
    close_bracket = text.find("]", open_bracket)
    if close_bracket == -1:
        return -1
    
    open_paren = text.find("(", close_bracket)
    if open_paren == -1 or open_paren != close_bracket + 1:
        return -1
    
    close_paren = text.find(")")
    if close_paren == -1:
        return -1
    
    return start_index, open_bracket, close_bracket, open_paren, close_paren, is_image

def create_delimited_node(text, delimiter):
    if delimiter == "*":
        node = HTMLNode("em", None)
    elif delimiter == "**":
        node = HTMLNode("strong", None)
    elif delimiter == "`":
        node = HTMLNode("code", None)
    
    node.children = text_to_children(text)
    return node

def create_link_node(link_text, url, is_image):
    if is_image:
        node = HTMLNode(
            tag="img",
            children=None,
            props= {"src": url, "alt": link_text}
                        )
    else:
        node = HTMLNode(
            tag="a",
            children = text_to_children(link_text),
            props={"href": url}
        )
    return node

def clean_quote_line(line):
    line = line.strip()
    if line.startswith('>'):
        line = line[1:].strip()
    return line

def process_quote_block(lines):
    quote_node = HTMLNode("blockquote")
    current_block = []
    
    # Remove the '>' prefix from each line
    cleaned_lines = [line.lstrip('> ').rstrip() for line in lines]
    
    for line in cleaned_lines:
        if not line.strip():  # Empty line - marks end of current block
            if current_block:
                # Process the current block
                if current_block[0].strip().startswith('-'):
                    # This is a list block
                    list_node = HTMLNode("ul")
                    for item in current_block:
                        if item.strip().startswith('-'):
                            item_text = item.lstrip('- ').strip()
                            list_item = HTMLNode("li", children=text_to_children(item_text))
                            list_node.children.append(list_item)
                    quote_node.children.append(list_node)
                else:
                    # This is a paragraph block
                    text = ' '.join(line.strip() for line in current_block)
                    para_node = HTMLNode("p", children=text_to_children(text))
                    quote_node.children.append(para_node)
                current_block = []
        else:
            current_block.append(line)
    
    # Don't forget to process the last block
    if current_block:
        if current_block[0].strip().startswith('-'):
            list_node = HTMLNode("ul")
            for item in current_block:
                if item.strip().startswith('-'):
                    item_text = item.lstrip('- ').strip()
                    list_item = HTMLNode("li", children=text_to_children(item_text))
                    list_node.children.append(list_item)
            quote_node.children.append(list_node)
        else:
            text = ' '.join(line.strip() for line in current_block)
            para_node = HTMLNode("p", children=text_to_children(text))
            quote_node.children.append(para_node)
    
    return quote_node

def create_list_item(content):
    return HTMLNode("li", children=text_to_children(content))

def text_to_children(text):
    nodes = [TextNode(text, TextType.NORMAL)]
    
    # Handle links
    result = []
    for node in nodes:
        link_indices = find_next_link(node.text)
        if link_indices == -1:
            result.append(node)
            continue
            
        start_index, open_bracket, close_bracket, open_paren, close_paren, is_image = link_indices
        
        # Get the parts
        text_before = node.text[:start_index + 1] if is_image else node.text[:start_index]
        link_text = node.text[open_bracket + 1:close_bracket]
        url = node.text[open_paren + 1:close_paren]
        text_after = node.text[close_paren + 1:]
        
        # Add text before link if it exists
        if text_before:
            result.append(TextNode(text_before, TextType.NORMAL))
            
        # Create link TextNode instead of HTMLNode
        result.append(TextNode(link_text, TextType.LINK, url))
        
        # Add text after link if it exists
        if text_after:
            result.append(TextNode(text_after, TextType.NORMAL))
            
    nodes = result
    
    
    # Handle inline code (`code`)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE, None)
    
    # Second pass - inline code (`code`)
    result = []
    for node in nodes:
        if node.text_type == TextType.CODE_BLOCK:
            result.append(node)
        else:
            inline_code_nodes = split_nodes_delimiter([node], "`", TextType.CODE, None)
            result.extend(inline_code_nodes)
    nodes = result
    
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD, None)

    # Third pass - italic
    result = []
    for node in nodes:
        if node.text_type == TextType.CODE:
            result.append(node)
        elif node.text_type == TextType.BOLD:
            # For bold nodes, process their text for italic
            italic_children = split_nodes_delimiter([TextNode(node.text, TextType.NORMAL)], "*", TextType.ITALIC, None)
            node.children = italic_children
            result.append(node)
        else:
            result.extend(split_nodes_delimiter([node], "*", TextType.ITALIC, None))
    
    # Convert TextNodes to HTMLNodes
    return [text_node_to_html_node(node) for node in result]


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown) #split markdown into blocks
    parent_node = HTMLNode(tag="div", children=[])

    for block in blocks:
        block_type = block_to_block_type(block)
        print(f"Block type: {block_type}")  # Debug print
        print(f"Block content: {block}")     # Debug print

        if block_type == "paragraph":
            paragraph_node = HTMLNode("p", text_to_children(block))
            parent_node.children.append(paragraph_node)
        
        elif block_type == "heading":
            level = 0
            for char in block:
                if char == '#':
                    level += 1
                else:
                    break
            
            text = block[level:].strip().strip('#').strip()
            heading_node = HTMLNode(f"h{level}", text_to_children(text))
            parent_node.children.append(heading_node)
        
        elif block_type == "quote":
            quote_content = block.lstrip('>').strip()
            quote_node = HTMLNode("blockquote", value=quote_content)
            parent_node.children.append(quote_node)


        elif block_type == "code":
            lines = block.split('\n')
            # Remove the triple backticks and join the remaining lines
            code_content = '\n'.join(lines[1:-1])
            
            # Create a single text node with CODE_BLOCK type
            text_node = TextNode(code_content, TextType.CODE_BLOCK)
            parent_node.children.append(text_node)

                
        elif block_type == "unordered_list":
            ul_node = HTMLNode("ul", [])
            lines = block.split('\n')
            for line in lines:
                if line.strip():
                    content = line.strip()[2:]  # Remove the '* ' or '- '
                    li_node = create_list_item(content)  # Use your create_list_item function
                    ul_node.children.append(li_node)
            parent_node.children.append(ul_node)

        elif block_type == "ordered_list":
            ol_node = HTMLNode(tag="ol", children=[])
            lines = block.split('\n')
            current_item = None
            current_text = ""
            
            for line in lines:
                stripped = line.strip()
                indentation = len(line) - len(line.lstrip())
                
                if not stripped:
                    continue
                    
                if indentation >= 3:  # Continuation line
                    if current_item and current_text:
                        current_text += " " + stripped
                        current_item.children = text_to_children(current_text)
                else:  # New list item
                    # Replace this if statement
                    # if line.strip().startswith(("1. ", "2. ", "3. ")):
                    # With the new logic:
                    parts = stripped.split('. ', 1)
                    if len(parts) == 2:
                        try:
                            item_number = int(parts[0])
                            current_text = parts[1]
                            current_item = HTMLNode("li", children=text_to_children(current_text))
                            ol_node.children.append(current_item)
                        except ValueError:
                            continue
            parent_node.children.append(ol_node)

    return parent_node
