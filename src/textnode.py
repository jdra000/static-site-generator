from enum import Enum
from htmlnode import HTMLNode, LeafNode, ParentNode
import re

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
		if self.url:
			return f"TextNode({self.text}, {self.text_type}, {self.url})"
		return f"TextNode({self.text}, {self.text_type})"




# Helper Methods
def extract_markdown_text(text, delimiter):
	matches = re.findall(fr"{re.escape(delimiter)}(.*?){re.escape(delimiter)}", text)
	return matches

def extract_markdown_images(text):
	tuples_list = []
	alt_text_matches = re.findall(r"\[(.*?)\]", text)
	url_matches = re.findall(r"\((.*?)\)", text)

	for i, alt_text in enumerate(alt_text_matches):
		tuples_list.append((alt_text, url_matches[i]))

	return tuples_list

def extract_markdown_links(text):
	tuples_list = []
	anchor_text_matches = re.findall(r"\[(.*?)\]", text)
	url_matches = re.findall(r"\((.*?)\)", text)

	for i, anchor_text in enumerate(anchor_text_matches):
		tuples_list.append((anchor_text, url_matches[i]))

	return tuples_list






def split_nodes_delimiter(old_nodes, delimiter, text_type):
	all_nodes = []

	for node in old_nodes:
		nodes_list = []

		if node.text_type != TextType.TEXT:
			nodes_list.append(node)
		else:
			matches = extract_markdown_text(node.text, delimiter)

			if matches:
				pattern = fr"({re.escape(delimiter)}.*?{re.escape(delimiter)})"
				sections = re.split(pattern, node.text)
				matches_count = 0

				for section in sections:
					text = matches[matches_count]

					if re.match(pattern, section):
						nodes_list.append(TextNode(text = text, text_type = text_type))

						if matches_count < len(matches)-1:
							matches_count += 1
					else:
						nodes_list.append(TextNode(text = section, text_type = TextType.TEXT))
			else:
				nodes_list.append(node)

		all_nodes.extend(nodes_list)

	return all_nodes


def split_nodes_images(old_nodes):
	all_nodes = []

	for node in old_nodes:
		nodes_list = []

		if node.text_type != TextType.TEXT:
			nodes_list.append(node)

		else:
			tuples_list = extract_markdown_images(node.text)

			if tuples_list:
				pattern = r"(!\[.*?\]\(.*?\))"
				sections = re.split(pattern, node.text)
				tuple_count = 0

				for section in sections:
					alt_text = tuples_list[tuple_count][0]
					url = tuples_list[tuple_count][1]

					if re.match(pattern, section):
						nodes_list.append(TextNode(text = alt_text, text_type = TextType.IMAGE, url = url))

						if tuple_count < len(tuples_list)-1:
							tuple_count += 1
					elif section.strip():
						nodes_list.append(TextNode(text = section, text_type = TextType.TEXT))
			else:
				nodes_list.append(node)

		all_nodes.extend(nodes_list)

	return all_nodes


def split_nodes_links(old_nodes):
	all_nodes = []

	for node in old_nodes:
		nodes_list = []

		if node.text_type != TextType.TEXT:
			nodes_list.append(node)

		else:

			tuples_list = extract_markdown_links(node.text)
			pattern = r"(\[.*?\]\(.*?\))"
			sections = re.split(pattern, node.text)

			if tuples_list:
				tuple_count = 0

				for section in sections:
					anchor_text = tuples_list[tuple_count][0]
					url = tuples_list[tuple_count][1]

					if re.match(pattern, section):
						nodes_list.append(TextNode(text = anchor_text, text_type = TextType.LINK, url = url))

						if tuple_count < len(tuples_list)-1:
							tuple_count += 1
					elif section.strip():
						nodes_list.append(TextNode(text = section, text_type = TextType.TEXT))

			else:
				nodes_list.append(node)

		all_nodes.extend(nodes_list)

	return all_nodes


def text_to_textnodes(text):
	all_nodes = [TextNode(text = text, text_type = TextType.TEXT)]

	# First split by Text Delimiters
	delimiters = {
		"**": TextType.BOLD, 
		"*": TextType.ITALIC, 
		"`": TextType.CODE}

	for key, value in delimiters.items():
		if split := split_nodes_delimiter(all_nodes, key, value):
			all_nodes = split

	# Finally split by Image and Link Delimiters
	if split := split_nodes_images(all_nodes):
		all_nodes = split
	if split := split_nodes_links(all_nodes):
		all_nodes = split

	return all_nodes



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








