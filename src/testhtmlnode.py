import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        #HTMLNode(tag,value,children,props)
        node1 = HTMLNode("b","WAKA WAKA",None,None)
        node2 = HTMLNode("a","www.lobsterrollexpress.com",None,{"href" : "lobsterroll.edu","target": "_blank"})
        node3 = HTMLNode("h1","HEADER",None,None)
        node4 = HTMLNode("body",None,(node1,node2,node3),None)

        #print(node1)
        #print(node2)
        #print(node2.props_to_html())
        #print(node3)
        #print(node4)


if __name__ == "__main__":
    unittest.main()