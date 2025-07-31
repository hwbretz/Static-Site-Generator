from enum import Enum
from htmlnode import *
import re

class TextType(Enum):            # markdown syntax
    TEXT = ("","plain")    # text
    BOLD = ("**","bold")    # **Bold text**
    ITALIC = ("_","italic") # _Italic text_
    CODE = ("`","code")     # `Code text`
    LINK = ("[","link")          # [anchor text](url)
    IMAGE = ("!","image")        # ![alt text](url)


#TextType = Enum('TextType',[('BOLD_TEXT',"**"),('ITALIC_TEXT',"_"),('CODE_TEXT',"'")])

class TextNode:
    
    def __init__(self,text,text_type = None,url = None):
        self.text = text
        
        self.url = url
        self.text_type = text_type
        # first time I made this to interpret text already in markdown
        if self.text_type is None:
            for typ in TextType:
                if text.startswith(typ.value[0]):# == text[0]:
                    self.text_type = typ

            if self.text_type == TextType.BOLD:
                self.text = text.replace("**","")

            elif self.text_type == TextType.ITALIC:
                self.text = text.replace("_","")

            elif self.text_type == TextType.CODE:
                self.text = text.replace("`","")

            elif self.text_type == TextType.LINK:
                #look for '('
                end_char_idx = 0
                while text[end_char_idx] != "(":
                    end_char_idx += 1
                #grab link, move up one to avoid '(', last character is ')'
                self.url = text[end_char_idx + 1:len(text) - 1]
                # first character is '[', move back 1 index from ')' to exclude ']'
                self.text = text[1:end_char_idx - 1]
                self.text= self.text.replace("(","")
            elif self.text_type == TextType.IMAGE:
                #look for '('
                end_char_idx = 0
                while text[end_char_idx] != "(":
                    end_char_idx += 1
                #grab link, move up one char to avoid '(', last character is ')'
                self.url = text[end_char_idx + 1:len(text) - 1]
                # first characters are '![', move back 1 index from ')' to exclude ']'
                self.text = text[2:end_char_idx - 1]
                self.text= self.text.replace("(","")
            else:
                self.text_type = TextType.TEXT
            
              

    def __eq__(self,text_two):
        if self.text == text_two.text:
            if self.text_type == text_two.text_type:
                if self.url == text_two.url:
                    return True

        return False

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value[1]}, {self.url})"

def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    if text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text)
    if text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text)
    if text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    if text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, {"href": text_node.url})
    if text_node.text_type == TextType.IMAGE:
        return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    raise ValueError(f"invalid text type: {text_node.text_type}")
        
def split_nodes_delimiter(old_nodes,delimiter,text_type):
    new_node_list = list()
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_node_list.append(node)
            continue
        split_nodes = list()
        string_splits = node.text.split(delimiter)
        #if len(string_splits) % 2 == 0: 
            #raise ValueError("unclosed section")
        for idx in range(len(string_splits)):
            if string_splits[idx] == "":
                continue
            if idx % 2 == 0:
                split_nodes.append(TextNode(string_splits[idx],TextType.TEXT))
            else:
                split_nodes.append(TextNode(string_splits[idx], text_type))
        new_node_list.extend(split_nodes)
    return new_node_list

def extract_markdown_images(text):
    alt_texts = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)",text)
    return alt_texts

def extract_markdown_links(text):
    alt_texts = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)",text)
    return alt_texts

def split_nodes_image(old_nodes):
    return_nodes = list()
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            return_nodes.append(node)
            continue
        original_text = node.text
        images = extract_markdown_images(original_text)
        if len(images) == 0:
            return_nodes.append(node)
            continue
        for image in images:
            sections = original_text.split(f"![{image[0]}]({image[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if sections[0] != "":
                return_nodes.append(TextNode(sections[0], TextType.TEXT))
            return_nodes.append(
                TextNode(
                    image[0],
                    TextType.IMAGE,
                    image[1],
                )
            )
            original_text = sections[1]
        if original_text != "":
            return_nodes.append(TextNode(original_text, TextType.TEXT))
    return return_nodes

def split_nodes_link(old_nodes):
    return_nodes = list()
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            return_nodes.append(node)
            continue
        original_text = node.text
        links = extract_markdown_links(original_text)
        if len(links) == 0:
            return_nodes.append(node)
            continue
        for link in links:
            sections = original_text.split(f"[{link[0]}]({link[1]})", 1)
            if len(sections) != 2:
                raise ValueError("invalid markdown, link section not closed")
            if sections[0] != "":
                return_nodes.append(TextNode(sections[0], TextType.TEXT))
            return_nodes.append(TextNode(link[0], TextType.LINK, link[1]))
            original_text = sections[1]
        if original_text != "":
            return_nodes.append(TextNode(original_text, TextType.TEXT))
    return return_nodes

def text_to_textnodes(text):
    new_nodes = [TextNode(text,TextType.TEXT)]
    new_nodes = split_nodes_delimiter(new_nodes,"_",TextType.ITALIC)
    new_nodes = split_nodes_delimiter(new_nodes,"`",TextType.CODE)
    new_nodes = split_nodes_delimiter(new_nodes,"**",TextType.BOLD)
    new_nodes = split_nodes_image(new_nodes)
    new_nodes = split_nodes_link(new_nodes)
    return new_nodes




    


