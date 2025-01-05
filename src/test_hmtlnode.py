import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
	def test_eq(self):
		node = HTMLNode("p", "pharagraph")
		node2 = HTMLNode("p", "pharagraph")
		self.assertEqual(node, node2)

	def test_not_eq(self):
		node = HTMLNode("a", "link", props={"href": "https://www.google.com"})
		node2 = HTMLNode("a", "new link")
		self.assertNotEqual(node, node2)

	def test_props_to_html(self):
		node = HTMLNode("a", "link", props={
			"href": "https://www.google.com", 
			"target": "_blank"})

		result = 'href="https://www.google.com" target="_blank"'
		self.assertEqual(node.props_to_html(), result)


class TestLeafNode(unittest.TestCase):
	def test_no_value(self):
		with self.assertRaises(ValueError):
			LeafNode(tag = "a", value = None, props={"href": "https://www.google.com"})

	def test_render_html(self):
		node = LeafNode(tag = "p", value = "Click me!")

		result = '<p>Click me!</p>'

		self.assertEqual(node.to_html(), result)

	def test_render_html_2(self):
		node = LeafNode(tag = "a", value = "Click me!", props={
			"href": "https://www.google.com"})

		result = '<a href="https://www.google.com">Click me!</a>'

		self.assertEqual(node.to_html(), result)

	def test_render_html_3(self):
		node = LeafNode(tag = "a", value = "Click me!", props={
			"href": "https://www.google.com",
			"target": "_blank"})

		result = '<a href="https://www.google.com" target="_blank">Click me!</a>'

		self.assertEqual(node.to_html(), result)


class TestParentNode(unittest.TestCase):
	def test_no_children(self):
		with self.assertRaises(ValueError):
			ParentNode("a", None)

	def test_no_tag(self):
		with self.assertRaises(ValueError):
			ParentNode(None, [LeafNode(tag = "b", value = "Bold text")])

	def test_render_html(self):
		node = ParentNode(tag = "p", children = [LeafNode(tag = "b", value = "Bold text"), LeafNode(tag = None, value = "Normal text")])

		result = '<p><b>Bold text</b>Normal text</p>'

		self.assertEqual(node.to_html(), result)

if __name__ == "__main__":
	unittest.main()









