import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

        node3 = TextNode("This is not a text node", TextType.BOLD)
        self.assertNotEqual(node, node3)

        node4 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node4)

        node5 = TextNode("Testing", TextType.LINK, "www.boot.dev")
        node6 = TextNode("Testing", TextType.LINK, "www.boot.dev")
        self.assertEqual(node5, node6)

if __name__ == "__main__":
    unittest.main()
