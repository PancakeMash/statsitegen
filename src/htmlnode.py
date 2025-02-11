from textnode import TextNode
class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children if children is not None else []
        self.props = props
    
    def to_html(self):
        if self.tag is None:
            if isinstance(self.value, (TextNode, HTMLNode)):
                return self.value.to_html()
            if isinstance(self.value, list):
                return "".join(v.to_html() if isinstance(v, (TextNode, HTMLNode)) else str(v) for v in self.value)
            return str(self.value) if self.value is not None else ""
        
        # Start with opening tag
        result = f"<{self.tag}{self.props_to_html()}>"
        
        # Add value if it exists
        if self.value is not None:
            if isinstance(self.value, (TextNode, HTMLNode)):
                result += self.value.to_html()
            elif isinstance(self.value, list):
                result += "".join(v.to_html() if isinstance(v, (TextNode, HTMLNode)) else str(v) for v in self.value)
            else:
                result += str(self.value)
        
        # Add children's HTML
        for child in self.children:
            result += child.to_html()
        
        # Add closing tag
        result += f"</{self.tag}>"
        
        return result
    
    def props_to_html(self):
        if not self.props:  # If self.props is None or empty
            return ""
    
        # Build the attributes string dynamically
        attributes = ""
        for key, value in self.props.items():
            attributes += f' {key}="{value}"'  # Add a leading space for proper formatting
        return attributes
    
    def __repr__(self):
        children_repr = [str(child) for child in self.children]
        return f"Tag: {self.tag}, Value: {self.value}, Children: [{', '.join(children_repr)}]"
    