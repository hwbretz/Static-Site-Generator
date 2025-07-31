import unittest

from textnode import *
from block import *

class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("**This is a text node**")
        node2 = TextNode("**This is a text node**")
        node3 = TextNode("[yo this link is wack yo](https://ball.ing/money)")
        node4 = TextNode("This is a text node")
        self.assertEqual(node, node2)
        self.assertNotEqual(node, node3)
        self.assertNotEqual(node,node3)

    def test_text(self):
        node = TextNode("This is a text node")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

        bold_node = TextNode("**BOLD**")
        html_bold_node = text_node_to_html_node(bold_node)
        self.assertEqual(html_bold_node.tag,"b")
        self.assertEqual(html_bold_node.value, "BOLD")

        italic_node = TextNode("_italic_")
        html_italic_node = text_node_to_html_node(italic_node)
        self.assertEqual(html_italic_node.tag,"i")
        self.assertEqual(html_italic_node.value, "italic")

        code_node = TextNode("`code`")
        html_bold_node = text_node_to_html_node(code_node)
        self.assertEqual(html_bold_node.tag,"code")
        self.assertEqual(html_bold_node.value, "code")

        link_node = TextNode("[link](www.google.com)")
        html_link_node = text_node_to_html_node(link_node)
        self.assertEqual(html_link_node.tag,"a")
        self.assertEqual(html_link_node.value,"link")
        self.assertEqual(html_link_node.props,{"href": "www.google.com"} )

        image_node = TextNode("![img_link](www.pictureOfSomething.com)")
        html_image_node = text_node_to_html_node(image_node)
        self.assertEqual(html_image_node.tag,"img")
        self.assertEqual(html_image_node.value,"")
        self.assertEqual(html_image_node.props,{"src": "www.pictureOfSomething.com","alt":"img_link"} )

    def test_split_nodes(self):
        code_node = TextNode("This is text with a `code block` word")
        split_nodes_code = split_nodes_delimiter([code_node],"`",TextType.CODE)
        #print(split_nodes_code)
        self.assertEqual("code block",split_nodes_code[1].text)
        self.assertEqual(split_nodes_code[1].text_type, TextType.CODE)


        italic_node = TextNode("This is text with a _italic block_ word")
        split_nodes_italic = split_nodes_delimiter([italic_node],"_",TextType.ITALIC)
        self.assertEqual("italic block",split_nodes_italic[1].text)
        self.assertEqual(split_nodes_italic[1].text_type, TextType.ITALIC)

        bold_node = TextNode("This is text with a **bold block** word")
        split_nodes_bold = split_nodes_delimiter([bold_node],"**",TextType.BOLD)
        self.assertEqual("bold block",split_nodes_bold[1].text)
        self.assertEqual(split_nodes_bold[1].text_type, TextType.BOLD)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)"
        )
        #print (matches)
        #self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

        matches_2 = extract_markdown_images("TEXTO ![](http://www.whoa.com/bigOlGif.png)")
        #print(matches_2)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with an [link](www.goggleyourgoogle.com)"
        )
        #print (matches)
        self.assertListEqual([("link", "www.goggleyourgoogle.com")], matches)

        matches_2 = extract_markdown_links("filler [](www.internet.com)")
        #print(matches_2)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

        node_2 = TextNode("![YO DOG](www.gangster.com) is the place to be homie.",TextType.TEXT)
        new_nodes_2 = split_nodes_image([node_2])
        #print(new_nodes_2)
        self.assertListEqual([TextNode("YO DOG",TextType.IMAGE,"www.gangster.com"),TextNode(" is the place to be homie.",TextType.TEXT)],new_nodes_2,)

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://www.google.com) and another [link2](wikipedia.org)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        #print(new_nodes)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://www.google.com"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "link2", TextType.LINK, "wikipedia.org"
                ),
            ],
            new_nodes,
        )

        node_2 = TextNode("[YO LINK](www.linkster.com) is the place to link homie.",TextType.TEXT,)
        #print(node_2)
        new_links_nodes = split_nodes_link([node_2])
        #print(new_nodes_2)
        self.assertListEqual([TextNode("YO LINK",TextType.LINK,"www.linkster.com"),TextNode(" is the place to link homie.",TextType.TEXT)],new_links_nodes,)
    
    def test_text_to_textnodes(self):
        nodes = text_to_textnodes(
            "This is **text** with an _italic_ word and a `code block` and an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)"
        )
        #for node in nodes:
            #print(node)

        self.assertListEqual(
                [
                    TextNode("This is ", TextType.TEXT),
                    TextNode("text", TextType.BOLD),
                    TextNode(" with an ", TextType.TEXT),
                    TextNode("italic", TextType.ITALIC),
                    TextNode(" word and a ", TextType.TEXT),
                    TextNode("code block", TextType.CODE),
                    TextNode(" and an ", TextType.TEXT),
                    TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                    TextNode(" and a ", TextType.TEXT),
                    TextNode("link", TextType.LINK, "https://boot.dev"),
                ],
                nodes,
            )    
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )    
    
    def test_blocktypes(self):
        block = "# heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        block = "> quote\n> more quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        block = "- list\n- items"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
        block = "1. list\n2. items"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
        block = "paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_paragraphs(self):
        md = """This is **bolded** paragraph\ntext in a p\ntag here\n\nThis is another paragraph with _italic_ text and `code` here\n"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
                html,
                "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
            )

    def test_codeblock(self):
        md = """```This is text that _should_ remain\nthe **same** even with inline stuff\n```"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        ) 
    
    def test_header_extraction(self):
        test_string = "# This is a header  "
        test_2_string = " This is a header  "
        self.assertNotEqual(extract_tile(test_2_string),extract_tile(test_string))

if __name__ == "__main__":
    unittest.main()