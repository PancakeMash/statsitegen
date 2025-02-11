from textnode import TextNode,TextType

def split_nodes_delimiter(old_nodes, delimiter, text_type, child_processor=None):
    node_list = []
    for node in old_nodes:
        if node.text_type != TextType.NORMAL:
            node_list.append(node)
            continue
        
        text = node.text
        start = text.find(delimiter)
        if start == -1:
            node_list.append(node)
            continue
            
        end = text.find(delimiter, start + len(delimiter))
        if end == -1:
            node_list.append(node)
            continue

        before = text[:start]
        middle = text[start + len(delimiter):end]
        after = text[end + len(delimiter):]

        if before:
            node_list.append(TextNode(before, TextType.NORMAL))
        if middle:
            print(f"Processing middle text: '{middle}'")
            print(f"Text type: {text_type}")
            print(f"Has child processor: {child_processor is not None}")
            # When processing nested formatting, keep the original text
            if child_processor and text_type != TextType.CODE and ("*" in middle or "`" in middle):
                children = child_processor(middle)
                middle_node = TextNode(middle, text_type, children)  # Keep the middle text
            else:
                middle_node = TextNode(middle, text_type)
            node_list.append(middle_node)
        if after:
            node_list.extend(split_nodes_delimiter([TextNode(after, TextType.NORMAL)], delimiter, text_type, child_processor))
    
    return node_list

def split_bold(node):
    return split_nodes_delimiter([node], "**", TextType.BOLD)

def split_italic(node):
    return split_nodes_delimiter([node], "*", TextType.ITALIC)

def split_code(node):
    return split_nodes_delimiter([node], "`", TextType.CODE)




