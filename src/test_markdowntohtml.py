import unittest
from parentnode import ParentNode
from leafnode import LeafNode
from markdowntohtml import *

def print_node_structure(node, indent=0):
    """Print the structure of an HTMLNode tree with indentation."""
    indent_str = "  " * indent
    if node.tag:
        print(f"{indent_str}{node.tag}:", end=" ")
    if node.value:
        print(f"'{node.value}'")
    else:
        print()
    
    for child in node.children:
        print_node_structure(child, indent + 1)

class TestParentNode(unittest.TestCase):
    def test_complex_quote(self):
        md = """> This is a *complex* quote
    > with **bold** and *italic* text
    > 
    > And a second paragraph
    > - with a list
    > - inside the quote"""

        # Print the processed output for debugging
        node = markdown_to_html_node(md)
        print_node_structure(node)  # If you have a debug function like this
        
        # You can also check the specific structure:
        assert node.tag == "div"
        quote_node = node.children[0]
        assert quote_node.tag == "blockquote"

if __name__ == "__main__":
    unittest.main()