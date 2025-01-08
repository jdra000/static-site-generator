from enum import Enum
from htmlnode import HTMLNode, LeafNode, ParentNode
import re, os

class TextType(Enum):
	TEXT = "normal"
	BOLD = "bold"
	ITALIC = "italic"
	CODE = "code"
	BLOCK_CODE = "block_code"
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
		"```":TextType.BLOCK_CODE,
		"`": TextType.CODE,
		"*": TextType.ITALIC,}

	for key, value in delimiters.items():
		if split := split_nodes_delimiter(all_nodes, key, value):
			all_nodes = split

	# Finally split by Image and Link Delimiters
	if split := split_nodes_images(all_nodes):
		all_nodes = split
	if split := split_nodes_links(all_nodes):
		all_nodes = split
	
	# Remove empty nodes
	all_nodes = [node for node in all_nodes if node.text.strip()]

	return all_nodes


def markdown_to_blocks(markdown):
	lines = markdown.split("\n")
	blocks = []
	string = ""
	is_code_block = False

	for line in lines:
		if line := line.strip():

			if line.startswith("```"):

				if is_code_block:
					string += " " + line 
					blocks.append(string.strip())

					is_code_block = False
					string = ""
				else:
					is_code_block = True
					string += " " + line 

			elif is_code_block:
				string += line + " "

			else:

				if (line[0] == "*" and line[1] != "*") or (line[0] == "-" and line[1] != "-") or (line[0].isdigit() and line[1] == "."):
					string += line +  " "

				else:
					if string:
						blocks.append(string.strip())
						blocks.append(line)
						string = ""
					else:
						blocks.append(line)
	if string:
		blocks.append(string.strip())

	return blocks


def block_to_block_type(block):
	if block.startswith("#"):
		return "heading"
	elif block.startswith("```") and block.endswith("```"):
		return "code"
	elif block.startswith(">"):
		return "quote"
	elif (block[0] == "*" and block[1] != "*") or (block[0] == "-" and block[1] != "*"):
		return "unordered list"
	elif block[0].isdigit():
		return "ordered list"
	else:
		return "normal"


def text_node_to_html_node(node, text_type):
	match (text_type):
		case TextType.TEXT:
			return LeafNode(value = node.text)
		case TextType.BOLD:
			return LeafNode(tag = "b", value = node.text)
		case TextType.ITALIC:
			return LeafNode(tag = "i", value = node.text)
		case TextType.CODE:
			return LeafNode(tag = "code", value = node.text)
		case TextType.BLOCK_CODE:

			node = LeafNode(tag = "code", value = node.text)
			return ParentNode(tag = "pre", children = [node])

		case TextType.LINK:
			return LeafNode(tag = "a", value = node.text, props = {"href": node.url})
		case TextType.IMAGE:
			return LeafNode(tag = "img", value= node.text, props = {"src": node.url, "alt": node.text})
		case _:
			raise Exception("No type found")


def block_to_html_node(block, block_category):
	match (block_category):
		case "heading":
			count = 1
			j = 1
			while (block[j]) == "#":
				count += 1
				j += 1

			block = block[count+1:]

			if nodes := text_to_textnodes(block):
				html_nodes = []

				for node in nodes:
					html_nodes.append(text_node_to_html_node(node, node.text_type))

			return ParentNode(tag = f"h{count}", children = html_nodes).to_html()

		case "unordered list":
			block = block[2:]

			unordered_blocks = block.split("- ")
			if len(unordered_blocks) < 2:
				unordered_blocks = block.split("* ")

			print(unordered_blocks)
			all_html_nodes = []

			for block in unordered_blocks:
				block = block.strip()

				if nodes := text_to_textnodes(block):
					html_nodes = []

					for node in nodes:
						html_nodes.append(text_node_to_html_node(node, node.text_type))

				all_html_nodes.extend([ParentNode(tag = "li", children = html_nodes)])

			return ParentNode(tag = f"ul", children = all_html_nodes).to_html()

		case "ordered list":
			block = block[3:]

			pattern = r"(\d+\.\s)"

			ordered_blocks = re.split(pattern, block)

			all_html_nodes = []

			for block in ordered_blocks:
				if re.match(pattern, block):
					ordered_blocks.remove(block)

			for block in ordered_blocks:
				block = block.strip()

				if nodes := text_to_textnodes(block):
					html_nodes = []
					for node in nodes:
						html_nodes.append(text_node_to_html_node(node, node.text_type))

				all_html_nodes.extend([ParentNode(tag = "li", children = html_nodes)])

			return ParentNode(tag = "ol", children = all_html_nodes).to_html()

		case "quote":
			block = block[2:]

			if nodes := text_to_textnodes(block):
				html_nodes = []

				for node in nodes:
					html_nodes.append(text_node_to_html_node(node, node.text_type))

		
			return ParentNode(tag = "blockquote", children = html_nodes).to_html()

		case "code":
			if nodes := text_to_textnodes(block):
				print(block)
				html_nodes = []

				print(nodes)
				for node in nodes:
					html_nodes.append(text_node_to_html_node(node, node.text_type))

		
			return "".join(node.to_html() for node in html_nodes)

		case "normal":

			if nodes := text_to_textnodes(block):
				html_nodes = []

				for node in nodes:
					html_nodes.append(text_node_to_html_node(node, node.text_type))

		
			return ParentNode(tag = "p", children = html_nodes).to_html()



def markdown_to_html_node(markdown):
	markdown_blocks = markdown_to_blocks(markdown)

	print(markdown_blocks)
	html_nodes = []
	for block in markdown_blocks:
		block_category = block_to_block_type(block)

		html_nodes.append(block_to_html_node(block, block_category))


	html_nodes.insert(0, "<div>")
	html_nodes.append("</div>")

	print(html_nodes)

	return "".join(html_nodes)


def generate_page(from_path, template_path, dest_path):
	print(f"Generating page from {from_path} to {dest_path} using {template_path}")

	with open(from_path, "r", encoding="utf-8") as file:
            markdown = file.read()
	
	with open(template_path, "r", encoding="utf-8") as file:
            template = file.read()
	
	html_content = markdown_to_html_node(markdown)

	final_html = template.replace("{{ Content }}", html_content)
	
	os.makedirs(os.path.dirname(dest_path), exist_ok=True)
	
	with open(dest_path, "w", encoding="utf-8") as file:
		file.write(final_html)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
	for item in os.listdir(dir_path_content):
		file_path = os.path.join(dir_path_content, item)

		if os.path.isfile(file_path):
			if file_path.endswith(".md"):
				
				relative_path = os.path.relpath(file_path, dir_path_content)

				dest_path = os.path.join(dest_dir_path, relative_path.replace(".md", ".html"))

				generate_page(file_path, template_path, dest_path)

		elif os.path.isdir(file_path):

			dest_dir = os.path.join(dest_dir_path, item)
			os.makedirs(dest_dir, exist_ok=True)

			generate_pages_recursive(file_path, template_path, dest_dir) 
		






