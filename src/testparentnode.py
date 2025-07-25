import unittest

from htmlnode import *

class TestParentNode(unittest.TestCase):
    def test_leaf_to_html(self):
        #def __init__(self, tag, children, props=None):
            #super().__init__(tag,None, children, props)
        node = ParentNode(
    "p",
    [
        LeafNode("b", "Bold text"),
        LeafNode(None, "Normal text"),
        LeafNode("i", "italic text"),
        LeafNode(None, "Normal text"),
    ],
)
        #print(node.to_html())
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        #print(parent_node.to_html())
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
    
    def test_node_equality(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        parent_node_2 = ParentNode("div",[child_node])
        self.assertNotEqual(child_node,parent_node)
        #self.assertEqual(parent_node,parent_node_2)

    def test_tree(self):
        grandchild_node = LeafNode("b", "grandchild")
        grandchild_node_2 = LeafNode("b","granchild_2")
        child_node = ParentNode("span", [grandchild_node])
        child_node_2 = ParentNode("span",[grandchild_node_2])
        parent_node = ParentNode("div", [child_node,child_node_2])
        #print(parent_node.to_html())

if __name__ == "__main__":
    unittest.main()