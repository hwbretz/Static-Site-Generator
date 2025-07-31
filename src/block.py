from textnode import *

def markdown_to_blocks(markdown):
    block_list = markdown.split("\n\n")
    for idx in range(0,len(block_list)):
        block_list[idx] = block_list[idx].strip()
    block_list_2 = list()
    for idx in range(0,len(block_list)):    
        if block_list !="":
            block_list_2.append(block_list[idx])

    return block_list_2
    
class BlockType(Enum):
    PARAGRAPH = "" # none below apply
    HEADING = "#"  # start with 1-6 # characters, followed by a space and then the heading text.
    CODE = "```"   # must start with 3 backticks and end with 3 backticks.
    QUOTE = ">"    # Every line in a quote block must start with a > character.
    UNORDERED_LIST = "-" # Every line in an unordered list block must start with a - character, followed by a space.
    ORDERED_LIST =  ["0",'1',"2","3","4","5","6","7","8","9"]  # Every line in an ordered list block must start with a number followed by a . character and a space. The number must start at 1 and increment by 1 for each line.

def block_to_block_type(block):
    lines = block.split("\n")
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

        
def markdown_to_html_node(markdown):
    #convert to blocks
    blocks = markdown_to_blocks(markdown)
    #determine type of block
    children = list()
    for block in blocks:
        html_node = block_to_html_node(block)
        children.append(html_node)
    return ParentNode("div",children,None)

def text_to_children(text):
    nodes = text_to_textnodes(text)
    chidrens = list()
    for node in nodes:
        chidrens.append(text_node_to_html_node(node))
    return chidrens

def block_to_html_node(block):
    type = block_to_block_type(block)
    
    if type == BlockType.HEADING:
        return heading_to_html_node(block)
    if type == BlockType.CODE:
        return code_to_html_node(block)
    if type == BlockType.ORDERED_LIST:
        return ordered_list_to_html(block)
    if type == BlockType.UNORDERED_LIST:
        return unordered_list_to_html(block)
    if type == BlockType.PARAGRAPH:
        return paragraph_to_html(block)
    if type == BlockType.QUOTE:
        return quote_to_html(block)
    raise ValueError("Error in block")

def heading_to_html_node(block):
    pounds = 0
    for character in block:
        if character == "#":
            pounds += 1
    if pounds + 1 > len(block):
        raise ValueError(f"Bad Header level: {pounds}")
    # get raw text
    text = block[pounds + 1:]
    children = text_to_children(text)
    return ParentNode(f"h{pounds}",children)

def code_to_html_node(block):
    if not block.startswith(BlockType.CODE.value) and not block.endswith(BlockType.CODE.value):
        raise ValueError("Improperly formatted Code Block")
    # get raw code text
    text = block[3:-3]
    text_node = TextNode(text,TextType.TEXT)
    child = text_node_to_html_node(text_node)
    codeNode = ParentNode("code",[child])
    return ParentNode("pre",[codeNode])

def quote_to_html(block):
    lines = block.split('\n')
    raw_lines = list()
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("Improperly Formatted Quote")
        #delete markdown char leading and trailing whitespace
        raw_lines.append(line.lstrip(">").strip())
    quote = " ".join(raw_lines)
    chidren = text_to_children(quote)
    return ParentNode("blockquote",chidren)

def unordered_list_to_html(block):
    lines = block.split('\n')
    html_lines = list()
    for line in lines:
        if not line.startswith("- "):
            raise ValueError("Improperly formatted unordered list")
        chidren = text_to_children((line[2:]))
        html_lines.append(ParentNode("li",chidren))
    return ParentNode("ul",html_lines)

def ordered_list_to_html(block):
    
    if block[0] not in BlockType.ORDERED_LIST.value:
        raise ValueError("Improperly Formatted list")
    item_count = int(block[0])
    lines = block.split('\n')
    html_lines = list()
    for line in lines:
        #if line[0] not in BlockType.ORDERED_LIST.value or line[1] != "." or int(line[0]) != item_count:
            #raise ValueError("Improperly Formatted list")
        chidren = text_to_children(line[3:])
        html_lines.append(ParentNode("li",chidren))
    return ParentNode("ol",html_lines)    

def paragraph_to_html(block):
    lines = block.split('\n')
    raw_text = " ".join(lines)
    chidren = text_to_children(raw_text)
    return ParentNode("p",chidren)



