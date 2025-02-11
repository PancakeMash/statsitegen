import unittest
from parentnode import ParentNode
from leafnode import LeafNode
from markdowntohtml import *

class TestParentNode(unittest.TestCase):
    def test_text_to_children(self):
        # Test 1: Basic formatting
        text1 = "This is **bold** and *italic* text"
        nodes1 = text_to_children(text1)
        
        # Test 2: Nested formatting
        text2 = "**Bold with *italic* inside**"
        nodes2 = text_to_children(text2)
        
        # Test 3: Code with formatting
        text3 = "Here is `code with **bold** inside` and *italic*"
        nodes3 = text_to_children(text3)
        
        # Test 4: Multiple nested elements
        text4 = "**Bold *with italic* and more bold** and *italic*"
        nodes4 = text_to_children(text4)

        print("\nTest results:")
        for i, nodes in enumerate([nodes1, nodes2, nodes3, nodes4], 1):
            print(f"\nTest {i}:")
            for node in nodes:
                print(f"Node: {node.tag}, Text: {node.value}")
                if node.children:
                    for child in node.children:
                        print(f"  Child: {child.tag}, Text: {child.value}")

if __name__ == "__main__":
    unittest.main()
    