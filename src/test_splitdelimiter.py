import unittest
from textnode import TextNode,TextType
from splitdelimiter import *

class TestSplitDelimiter(unittest.TestCase):
    def test_basecase(self):
        node = TextNode("This is text with a `code block` word", TextType.NORMAL)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_result = [TextNode("This is text with a ", TextType.NORMAL),
                           TextNode("code block", TextType.CODE),
                           TextNode(" word", TextType.NORMAL)]
        self.assertEqual(new_nodes, expected_result)

    def test_basecase2(self):
        node2 = TextNode("This is text with a **bold** word", TextType.NORMAL)
        new_nodes2 = split_nodes_delimiter([node2], "**", TextType.BOLD)
        expected_result2 = [TextNode("This is text with a ", TextType.NORMAL),
                           TextNode("bold", TextType.BOLD),
                           TextNode(" word", TextType.NORMAL)]
        self.assertEqual(new_nodes2, expected_result2)
    
    #def test_missingdelimit(self):
    #    with self.assertRaises(Exception):
    #        node = TextNode("This is a text with *italics in it", TextType.NORMAL)
    #        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
    
    def test_incorrect_type(self):
        node = TextNode("This is text with a `code block` word", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_result = [TextNode("This is text with a `code block` word", TextType.BOLD)]
        self.assertEqual(new_nodes, expected_result)

    
if __name__ == "__main__":
    unittest.main()