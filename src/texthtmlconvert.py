from textnode import TextType
from leafnode import LeafNode
from htmlnode import HTMLNode


def text_node_to_leaf_node(text_node):
    match(text_node.text_type):
        case TextType.NORMAL:
            return LeafNode("", text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, text_node.url)
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        
        case _:
            raise Exception


def text_node_to_html_node(text_node):
    # Process any children first
    children = []
    if text_node.children:
        children = [text_node_to_html_node(child) for child in text_node.children]
        # When we have children, we still need to process the text
        # The text should be used to create the appropriate HTML structure
        value = text_node.text
    else:
        value = text_node.text
    
    match(text_node.text_type):
        case TextType.NORMAL:
            return HTMLNode(None, value, children)
        case TextType.BOLD:
            if text_node.children:
                # If we have children, don't use the original text
                return HTMLNode("b", None, children)
            else:
                # If no children, use the text value
                return HTMLNode("b", value)
        case TextType.ITALIC:
            # For italic text, we want the content as a child node
            if not children:
                children = [HTMLNode(None, value)]
                value = None
            return HTMLNode("i", value, children)
        case TextType.CODE_BLOCK:
            return HTMLNode("pre", None, [HTMLNode("code", text_node.text)])
        case TextType.CODE:
            return HTMLNode("code", text_node.text)
        case TextType.LINK:
            return HTMLNode("a", text_node.text, props={"href": text_node.url})
        case TextType.IMAGE:
            return HTMLNode("img", "", children, {"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception