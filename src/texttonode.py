from extractlinks import *
from splitdelimiter import *

#example = 'This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)'
#The goal is to parse through this string and build a series of TextNodes.
#Put all nodes into a single list and parse through each. Also put the string into a TextNode first.
#Figure out how to appropriately loop through each node whilst maintaining string order.

def split_image(node):
    return split_nodes_image([node])

def split_link(node):
    return split_nodes_link([node])


def text_to_node(text):
    nodes = [TextNode(text, TextType.NORMAL)]

    split_functions = [
        split_bold,
        split_italic,
        split_code,
        split_image,
        split_link
    ]

    result_nodes = nodes
    for split_func in split_functions:
        new_nodes = []
        for node in result_nodes:
            if node.text_type == TextType.NORMAL:
                split_result = split_func(node)
          #      print(f"Split {node.text} with {split_func.__name__}:")
         #       print(f"Result: {split_result}")
                new_nodes.extend(split_result)
            else:
                new_nodes.append(node)
        result_nodes = new_nodes
        #print(f"\nAfter {split_func.__name__}:")
        #print(result_nodes)
        #print("-------------------")
    
    return result_nodes

#test = text_to_node(example)
#print(test)