from textnode import TextType, TextNode

def main():
	text_node = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
	print(text_node.__repr__())



main()