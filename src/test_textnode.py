import unittest

from textnode import TextType, TextNode, text_node_to_html_node
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

	# Test function
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