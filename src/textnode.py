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
        if text_node.text_type == TextType.BOLD:
            return LeafNode("b",text_node.text)
        
        elif text_node.text_type == TextType.ITALIC:
           return LeafNode("i",text_node.text)
        
        elif text_node.text_type == TextType.CODE:
            return LeafNode("code",text_node.text)
        
        elif text_node.text_type == TextType.LINK:
            return LeafNode("a",text_node.text,{"href":text_node.url})
        
        elif text_node.text_type == TextType.IMAGE:
            return LeafNode("img","",{"src":text_node.url,"alt":text_node.text})
        
        else:
            return LeafNode(None,text_node.text)
        
def split_nodes_delimiter(old_node,text_type):
    new_node_list = list()
    #have to do [0][0:] for bold character **
    string_splits = old_node.text.split(text_type.value[0][0:])
    #print(text_type.value[0])
    #print(string_splits)
    for string_section in string_splits:
        #print(string_section)
        if string_section[0] == " " or string_section[len(string_section) - 1] == " ":
            new_node_list.append(TextNode(string_section,TextType.TEXT))
        else:
            new_node_list.append(TextNode(string_section,text_type))
    return new_node_list

def extract_markdown_images(text):
    alt_texts = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)",text)
    #alt_texts = alt_texts = re.findall(r"!\[(.*?)\]\((.*?)\)",text)
    #print(alt_texts)
    
    return alt_texts

def extract_markdown_links(text):
    alt_texts = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)",text)
    #print(alt_texts)
    
    return alt_texts

def split_nodes_image(old_nodes):
    return_nodes = list()
    for node in old_nodes:
        #pull image text and link from node.text
        links = extract_markdown_images(node.text)
        link_count = 0
        start_char = 0

        for end_char in range(0,len(node.text)):
            #image reached
            if node.text[end_char] == "!":
                #plain text section
                if start_char < end_char:
                    return_nodes.append(TextNode(node.text[start_char:end_char],TextType.TEXT))
                    
                #add node with data from links list
                return_nodes.append(TextNode(links[link_count][0],TextType.IMAGE,links[link_count][1]))
                link_count += 1

                #advance idx to past end of link
                while node.text[end_char] != ")":
                    end_char += 1

                #start of new string subsection
                start_char = end_char + 1

            # non image link end of string
            elif end_char == len(node.text) - 1 and node.text[end_char] != ")":
                return_nodes.append(TextNode(node.text[start_char:end_char+1],TextType.TEXT))
                
    return return_nodes

def split_nodes_link(old_nodes):
    return_nodes = list()
    for node in old_nodes:
        # extract links and assocaiated text from node
        links = extract_markdown_links(node.text)
        #track link count to use appropriate values in order
        link_count = 0
        #for building strings 
        start_char = 0

        for end_char in range(0,len(node.text)):
            #link reached
            if node.text[end_char] == "[":
                #plain text section
                if start_char < end_char:     
                    return_nodes.append(TextNode(node.text[start_char:end_char],TextType.TEXT))
                    
                #add node with data from links list, advance through links list
                return_nodes.append(TextNode(links[link_count][0],TextType.LINK,links[link_count][1]))
                link_count += 1

                #advance idx to past end of link
                while node.text[end_char] != ")":
                    end_char += 1

                #start of new string subsection
                start_char = end_char + 1
                
            # non link end of string
            elif end_char == len(node.text) - 1 and node.text[end_char] != ")":
                return_nodes.append(TextNode(node.text[start_char:end_char+1],TextType.TEXT))

    return return_nodes

    


