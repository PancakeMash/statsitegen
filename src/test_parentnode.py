import unittest
from parentnode import ParentNode
from leafnode import LeafNode

class TestParentNode(unittest.TestCase):
    def test_base_case(self):
        node = ParentNode('p',[LeafNode("b", "Bold text"),LeafNode(None, "Normal text"),LeafNode("i", "italic text"),LeafNode(None, "Normal text")])
        generated_html = node.to_html()
        #print(generated_html)
        expected_result = '<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>'
        self.assertEqual(generated_html, expected_result)

    def test_base_case2(self):
        node2 = ParentNode('p', [LeafNode("b", "Bold text"), LeafNode(None, "Normal text")])
        generated_html2 = node2.to_html()
        expected_result2 = '<p><b>Bold text</b>Normal text</p>'
        self.assertEqual(generated_html2, expected_result2)
    
    def test_no_tags(self):
        with self.assertRaises(ValueError) as context:
            node3 = ParentNode(None, [LeafNode("b", "Bold text")])
            node3.to_html()
    
    def test_no_children(self):
        with self.assertRaises(ValueError) as context:
            node4 = ParentNode("b", [])
            node4.to_html()
    
    def test_case3(self):
        with self.assertRaises(ValueError) as context:
            node5 = ParentNode('p', [LeafNode("b", "")])
            node5.to_html()

if __name__ == "__main__":
    unittest.main()
