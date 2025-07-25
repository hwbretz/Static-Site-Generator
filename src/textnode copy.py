from enum import Enum



#TextType = Enum('TextType',[('BOLD_TEXT',"**"),('ITALIC_TEXT',"_"),('CODE_TEXT',"'")])

class TextNode:
    class TextType(Enum):            # markdown syntax
        PLAIN_TEXT = ("","plain")    # text
        BOLD_TEXT = ("*","bold")    # **Bold text**
        ITALIC_TEXT = ("_","italic") # _Italic text_
        CODE_TEXT = ("'","code")     # `Code text`
        LINK = ("[","link")          # [anchor text](url)
        IMAGE = ("!","image")        # ![alt text](url)

    def __init__(self,text):
        self.text = text
        self.text_type = self.TextType.PLAIN_TEXT
        #print(self.text_type)
        self.url = None
        #if text[0] in TextType.value:
        for typ in self.TextType:
            if typ.value[0] == text[0]:
                self.text_type = typ
                

        if self.text_type == self.TextType.BOLD_TEXT:
            self.text = text.replace("**","")

        elif self.text_type == self.TextType.ITALIC_TEXT:
            self.text = text.replace("_","")

        elif self.text_type == self.TextType.CODE_TEXT:
            self.text = text.replace("'","")

        elif self.text_type == self.TextType.LINK:
            #look for '('
            end_char_idx = 0
            while text[end_char_idx] != "(":
                end_char_idx += 1
            #grab link, last character is ')'
            self.url = text[end_char_idx:len(text) - 1]
            # first character is '[', move back 1 index from ')' to exclude ']'
            self.text = text[1:end_char_idx - 1]
        elif self.text_type == self.TextType.IMAGE:
            #look for '('
            end_char_idx = 0
            while text[end_char_idx] != "(":
                end_char_idx += 1
            #grab link, last character is ')'
            self.url = text[end_char_idx:len(text) - 1]
            # first characters are '![', move back 1 index from ')' to exclude ']'
            self.text = text[2:end_char_idx - 1]

    def __eq__(self,text_one,text_two):
        if text_one.text == text_two.text:
            if text_one.text_type == text_two.text_type:
                if text_one.url == text_two.url:
                    return True

        return False

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value[1]}, {self.url})"
