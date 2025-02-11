from htmlnode import HTMLNode
from leafnode import LeafNode

class ParentNode(HTMLNode):
    def __init__(self, tag, children):
        super().__init__(tag, None, children, None)
    
    def to_html(self):
        if not self.tag:
            raise ValueError("no tag value")
        if not self.children:
            raise ValueError("no children value")
        
        html_string = ""
        for child in self.children:
            recursive_results = child.to_html()
            html_string = html_string + recursive_results
        return f'<{self.tag}>{html_string}</{self.tag}>'
        