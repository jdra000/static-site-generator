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
	text_to_textnodes)

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
	def test_split_nodes_delimiter_bold(self):
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


	# text_node_to_html_node function
	def test_text_node_to_html_node(self):
		node = text_node_to_html_node(TextType.TEXT)
		self.assertIsInstance(node, LeafNode)

		node = text_node_to_html_node(TextType.LINK)
		self.assertIsInstance(node, LeafNode)
		self.assertEqual(node.props.get("href"), "https://www.google.com")

		node = text_node_to_html_node(TextType.IMAGE)
		self.assertIsInstance(node, LeafNode)
		self.assertEqual(node.props.get("src"), "url/image")
		self.assertEqual(node.props.get("alt"), "brief description")

if __name__ == "__main__":
	unittest.main()