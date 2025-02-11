import unittest
from leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_para_case(self):
        node = LeafNode("p", "This is a paragraph of text.")
        assert node.to_html() == '<p>This is a paragraph of text.</p>'
    
    def test_html_case(self):
        node2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        print("props_to_html:", node2.props_to_html())
        assert node2.to_html() == '<a href="https://www.google.com">Click me!</a>'
    
    def test_no_value_para(self):
        node3 = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node3.to_html()
    
    def test_no_tag_para(self):
        node4 = LeafNode(None, "I like pancakes")
        print("to_html:", node4.to_html())
        assert node4.to_html() == 'I like pancakes'
    
    def test_no_tag_html(self):
        node5 = LeafNode(None, "Click me!", {"href": "https://www.google.com"})
        assert node5.to_html() == "Click me!"

if __name__ == "__main__":
    unittest.main()