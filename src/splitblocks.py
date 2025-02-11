from texttonode import *

def markdown_to_blocks(markdown):
    blocks = []
    current_block = []
    in_code_block = False
    
    for line in markdown.split("\n"):
        # Toggle code block state
        if line.strip().startswith("```"):
            in_code_block = not in_code_block
            
        # If we hit an empty line and not in code block
        if len(line.strip()) == 0 and not in_code_block:
            # If we have a current block, join it and add to blocks
            if current_block:
                blocks.append("\n".join(current_block))
                current_block = []
        else:
            # Add the line as-is, preserving whitespace
            current_block.append(line)
    
    # Don't forget last block
    if current_block:
        blocks.append("\n".join(current_block))
    
    return blocks


def block_to_block_type(mark):
    print(repr(mark))

    #mark = markdown_to_blocks(markdown)
    if mark.startswith("#"):
        text_after_prefix = mark[mark.count("#") + 1:].strip()
        if (0 < mark.count("#") <= 6 and 
            len(mark) > mark.count("#") and 
            mark[mark.count("#")] == " " and 
            text_after_prefix):
            return "heading"
        
     # New code block check
    lines = mark.splitlines()
    if len(lines) >= 2:  # Need at least opening, content, and closing
        first_line = lines[0].strip()
        last_line = lines[-1].strip()
        if first_line.startswith('```') and last_line == '```':
            return "code"
    
    if (mark.startswith(">") or   # Remove the elif here
      all(line.strip().startswith(">") for line in mark.splitlines())):
        print("Found quote block!")
        print("Lines:", [line.strip() for line in mark.splitlines()])
        return "quote"
    
    elif (mark.startswith("*") and mark[1] == " ") or mark.startswith("-") and mark[1] == " ":
        return "unordered_list"
    
    lines = mark.splitlines()
    first_line = lines[0].strip()
    print(f"First line: '{first_line}'")  # Debug
    
    if first_line.startswith("1. "):  # Must start with 1
        expected_number = 1
        for line in lines:
            print(f"Line: '{line}'")  # Show raw line
            print(f"Indentation: {len(line) - len(line.lstrip())}")  # Show spaces


            stripped = line.strip()
            print(f"Checking line: '{stripped}'")  # Debug
            if not stripped:  # Skip empty lines
                continue
            if len(line) - len(line.lstrip()) >= 3:  # Indented continuation
                print("Found continuation line")
                continue

            # Check if it's the next number in sequence
            print(f"Expecting number: {expected_number}")  # Debug
            if not stripped.startswith(f"{expected_number}. "):
                print(f"Failed at: {stripped}")  # Debug
                return "paragraph"
            expected_number += 1
        return "ordered_list"

    return "paragraph"