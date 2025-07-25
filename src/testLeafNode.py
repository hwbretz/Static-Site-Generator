import unittest

from htmlnode import *

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html(self):
        #(self,tag,value,props=None)
        node = LeafNode("p","Hello, World!")
        self.assertEqual(node.to_html(),"<p>Hello, World!</p>")
        node2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        #print(node2.to_html())
        node3 = LeafNode(None,"plain text")
        self.assertEqual(node3.to_html(),"plain text")

if __name__ == "__main__":
    unittest.main()