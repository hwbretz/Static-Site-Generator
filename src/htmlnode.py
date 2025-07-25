
class HTMLNode:
    def __init__(self,tag=None,value=None,children=None,props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
        
    
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        prop_str = ""
        if self.props is not None:
            for k,v in self.props.items():
                prop_str += f' {k}="{v}"'
            return prop_str
        else:
            return "No props"

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
            raise ValueError
        if self.tag == None:
            return self.value
        else:
            html_str = f"<{self.tag}"
            if self.props is not None:
                html_str += self.props_to_html()
            html_str += f">{self.value}</{self.tag}>"
            return html_str
    
class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag,None, children, props)

    def to_html(self):
        #return super().to_html()
        if self.tag == None:
            raise ValueError
        for child in self.children:
            if child.value == None and not isinstance(child,ParentNode):
                raise ValueError(f"Child missing value")
        html_str = f"<{self.tag}>"
        if self.children is not None:
            for child in self.children:
                html_str += child.to_html()
        html_str += f"</{self.tag}>"
        return html_str

