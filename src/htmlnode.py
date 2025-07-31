
class HTMLNode:
    def __init__(self,tag=None,value=None,children=None,props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
        
    
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if self.props is None:
            return ""
        props_html = ""
        for prop in self.props:
            props_html += f' {prop}="{self.props[prop]}"'
        return props_html
    
    def __repr__(self):
        node_str = ""
        if self.tag is not None:
            node_str += f"Tag: {self.tag}, "
        else:
            node_str +="No Tag, "

        if self.value is not None:
            node_str += f"Value: {self.value}, "
        else:
            node_str += "No Value, "

        if self.children is not None:
            node_str += f"Children: "
            for child in self.children:
                node_str += f"\n\t{child}"
        else:
            node_str += "No Children, "
        
        if self.props is not None:
            node_str += "Props: "
            node_str += f"\n\t{self.props_to_html()}"
        else:
            node_str += "No Props"
        
        return node_str
    
class LeafNode(HTMLNode):
    def __init__(self,tag,value,props=None):
        super().__init__(tag,value,None,props)

    def to_html(self):
        if self.value == None:
            raise ValueError("invalid HTML: no value")
        if self.tag == None:
            return self.value
        else:
           return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        
    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag,None, children, props)

    def to_html(self):
        #return super().to_html()
        if self.tag == None:
            raise ValueError("invalid: no tag")
        if self.children is None:
            raise ValueError("invalid: no children")
        children_html = ""
        for child in self.children:
            children_html += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"

    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"



