from enum import Enum

class TextType(Enum):
    NORMAL = "normal"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"
    CODE_BLOCK = "code_block"

class TextNode:
    def __init__(self, text, text_type, url=None, children=None):
        self.text = text
        self.text_type = text_type
        self.url = url
        self.children = children if children is not None else []
    
    def escape_html(self, text):
     return (text
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )
    
    def to_html(self):
        if self.text_type == TextType.NORMAL:
            return self.text
        elif self.text_type == TextType.BOLD:
            return f"<b>{self.text}</b>"
        elif self.text_type == TextType.ITALIC:
            return f"<i>{self.text}</i>"
        elif self.text_type == TextType.CODE:
            escaped_text = self.escape_html(self.text)
            return f"<code>{escaped_text}</code>"
        elif self.text_type == TextType.CODE_BLOCK:
            escaped_text = self.escape_html(self.text)
            return f"<pre><code>{escaped_text}</code></pre>"
        elif self.text_type == TextType.LINK:
            return f'<a href="{self.url}">{self.text}</a>'
        else:
            raise ValueError(f"Invalid text type: {self.text_type}")

    def __eq__(self, other):
        if (self.text == other.text 
        and self.text_type == other.text_type 
        and self.url == other.url):
            return True
        return False
    
    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"
