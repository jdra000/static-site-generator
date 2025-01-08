from textnode import TextType, TextNode, generate_page, generate_pages_recursive
import os
import shutil

def main():
	text_node = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
	print(text_node.__repr__())



main()


def construct_directory(source, destination):

	destination_paths = os.listdir(destination)

	for item in os.listdir(destination):
		file_path = os.path.join(destination, item)
		if os.path.isfile(file_path):
			os.unlink(file_path)

		elif os.path.isdir(file_path):
			shutil.rmtree(file_path)  

	for item in os.listdir(source):
		source_path = os.path.join(source, item)
		destination_path = os.path.join(destination, item)

		if os.path.isfile(source_path):
			shutil.copy(source_path, destination_path)

		elif os.path.isdir(source_path):

			shutil.copytree(source_path, destination_path)


construct_directory("/Users/juanrey/workspace/github.com/JDRA000/static-site-generator/static", "/Users/juanrey/workspace/github.com/JDRA000/static-site-generator/public")

generate_pages_recursive(
	"./content",
	"./template.html",
	"./public")

