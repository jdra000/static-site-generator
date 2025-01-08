import unittest

# textnode classes
from textnode import TextType, TextNode

# textnode functions
from textnode import(
	text_node_to_html_node, 
	split_nodes_delimiter, extract_markdown_images, 
	extract_markdown_links,
	split_nodes_images,
	split_nodes_links,
	text_to_textnodes,
	markdown_to_blocks,
	block_to_block_type,
	markdown_to_html_node)

from htmlnode import LeafNode

class TestTextNode(unittest.TestCase):
	def test_eq(self):
		node = TextNode("This is a text node", TextType.BOLD)
		node2 = TextNode("This is a text node", TextType.BOLD)
		self.assertEqual(node, node2)

	def test_not_eq(self):
		node = TextNode("This is a text node", TextType.BOLD)
		node2 = TextNode("This is a different node", TextType.BOLD)
		self.assertNotEqual(node, node2)

	def test_text_type(self):
		node = TextNode("This is a text node", TextType.BOLD)
		self.assertIsInstance(node.text_type, TextType)

	# split_nodes_delimiter function
	def test_split_nodes_delimiter(self):
		node1 = TextNode("This is text with a **bold block** word", TextType.TEXT)
		node2 = TextNode("This is text with a **bold sentence** phrase", TextType.TEXT)

		new_nodes = split_nodes_delimiter([node1, node2], "**", TextType.BOLD)

		expected_nodes = [
  			TextNode("This is text with a ", TextType.TEXT),	
  			TextNode("bold block", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold sentence", TextType.BOLD),
            TextNode(" phrase", TextType.TEXT)
        ]
		self.assertEqual(new_nodes, expected_nodes)

	# split_nodes_images function
	def test_split_nodes_images(self):
		node = TextNode("This is text with an image ![to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev)", TextType.TEXT)

		new_nodes = split_nodes_images([node])

		expected_nodes = [
			TextNode("This is text with an image ", TextType.TEXT),
			TextNode("to boot dev", TextType.IMAGE, "https://www.boot.dev"),
			TextNode(" and ", TextType.TEXT),
			TextNode("to youtube", TextType.IMAGE, "https://www.youtube.com/@bootdotdev")
		]

		self.assertEqual(new_nodes, expected_nodes)


	def test_split_nodes_links(self):
		node = TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)", TextType.TEXT)

		new_nodes = split_nodes_links([node])

		expected_nodes = [
			TextNode("This is text with a link ", TextType.TEXT),
			TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
			TextNode(" and ", TextType.TEXT),
			TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev")
		]

		self.assertEqual(new_nodes, expected_nodes)


	def test_text_to_textnodes(self):
		text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"

		new_nodes = text_to_textnodes(text)

		expected_nodes = [
		    TextNode("This is ", TextType.TEXT),
		    TextNode("text", TextType.BOLD),
		    TextNode(" with an ", TextType.TEXT),
		    TextNode("italic", TextType.ITALIC),
		    TextNode(" word and a ", TextType.TEXT),
		    TextNode("code block", TextType.CODE),
		    TextNode(" and an ", TextType.TEXT),
		    TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
		    TextNode(" and a ", TextType.TEXT),
		    TextNode("link", TextType.LINK, "https://boot.dev"),
		]
		
		self.assertEqual(new_nodes, expected_nodes)


	def test_markdown_to_blocks(self):
		text = """# This is a heading

		This is a paragraph of text. It has some **bold** and *italic* words inside of it.

		* This is the first list item in a list block
		* This is a list item
		* This is another list item"""

		result_list = markdown_to_blocks(text)

		expected_list = [
			"# This is a heading",
			"This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
			"* This is the first list item in a list block * This is a list item * This is another list item"
		]

		self.assertEqual(result_list, expected_list)


	def test_block_to_block_type(self):
		markdown_blocks = [
		    "# Heading 1",
		    "```python\nprint('Hello World!')\n```",
		    "> This is a quote",
		    "* Unordered list item 1",
		    "- Unordered list item 2",
		    "1. Ordered list item 1",
		    "Normal text"
		]

		expected_block_types = [
		"heading",
		"code",
		"quote",
		"unordered list",
		"unordered list",
		"ordered list",
		"normal",
		]		

		for i, block in enumerate(markdown_blocks):
		    category = block_to_block_type(block)

		    self.assertEqual(category, expected_block_types[i])


	# extract_markdown_images function
	def test_extract_markdown_images(self):
		text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
		result = extract_markdown_images(text)
		expected_result = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]

		self.assertEqual(result, expected_result)

	# extract_markdown_links function
	def test_extract_markdown_links(self):
		text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
		result = extract_markdown_links(text)
		expected_result = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]

		self.assertEqual(result, expected_result)



	def test_markdown_to_html_node(self):
		markdown = """# Introduction to Markdown

Markdown is a **lightweight markup language** that you can use to format text. It's widely used in *writing documentation* and creating content for the web.

Here are some key features:
	
- You can create **bold** text using `**` or `__`.
- Italics are created using `*` or `_` for *emphasis*.
- [Markdown Guide](https://www.markdownguide.org) is a great resource to learn more.

Happy writing!
"""
		result = markdown_to_html_node(markdown)

		expected_result = """<div><h1>Introduction to Markdown</h1><p>Markdown is a <b>lightweight markup language</b> that you can use to format text. It's widely used in <i>writing documentation</i> and creating content for the web.</p><p>Here are some key features:</p><ul><li>You can create <b>bold</b> text using <code>**</code> or <code>__</code>.</li><li>Italics are created using <code>*</code> or <code>_</code> for <i>emphasis</i>.</li><li><a href="https://www.markdownguide.org">Markdown Guide</a> is a great resource to learn more.</li></ul><p>Happy writing!</p></div>"""

		self.assertEqual(result, expected_result)





if __name__ == "__main__":
	unittest.main()