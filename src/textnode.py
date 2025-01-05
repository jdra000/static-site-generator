from enum import Enum
from htmlnode import HTMLNode, LeafNode, ParentNode

class TextType(Enum):
	TEXT = "normal"
	BOLD = "bold"
	ITALIC = "italic"
	CODE = "code"
	LINK = "link"
	IMAGE = "image"

class TextNode():
	def __init__(self, text, text_type: TextType, url = None):
		self.text = text
		self.text_type = text_type
		self.url = url

	def __eq__(self, TextNode):
		if self.text == TextNode.text and self.text_type == TextNode.text_type and self.url == TextNode.url:
			return True
		return False

	def __repr__(self):
		return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


def text_node_to_html_node(text_node):
	match (text_node):
		case TextType.TEXT:
			return LeafNode(value = "testing")
		case TextType.BOLD:
			return LeafNode(tag = "b", value = "testing")
		case TextType.ITALIC:
			return LeafNode(tag = "i", value = "testing")
		case TextType.CODE:
			return LeafNode(tag = "code", value = "testing")
		case TextType.LINK:
			return LeafNode(tag = "a", value = "testing", props = {"href": "https://www.google.com"})
		case TextType.IMAGE:
			return LeafNode(tag = "img", value= " ", props = {"src": "url/image", "alt": "brief description"})
		case _:
			raise Exception("No type found")
