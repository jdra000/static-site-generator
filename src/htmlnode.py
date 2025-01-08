class HTMLNode():
	def __init__(self, tag = None, value = None, children = None, props = None):
		self.tag = tag
		self.value = value
		self.children = children
		self.props = props

	def to_html(self):
		raise NotImplementedError

	def props_to_html(self):
		return " ".join(f'{key}="{value}"' for key, value in self.props.items())

	def __repr__(self):
		return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props_to_html()})"


	def __eq__(self, HTMLNode):
		if self.tag == HTMLNode.tag and self.value == HTMLNode.value and self.children == HTMLNode.children and self.props == HTMLNode.props:
			return True
		return False

class LeafNode(HTMLNode):
	def __init__(self, value, tag = None, props = None):
		if not value:
			raise ValueError("value is required")
		super().__init__(tag = tag, value = value, children = None, props = props)

	def to_html(self):
		if not self.tag:
			return self.value

		if not self.props:
			return f"<{self.tag}>{self.value}</{self.tag}>"
		
		return f"<{self.tag} {self.props_to_html()}>{self.value}</{self.tag}>"

class ParentNode(HTMLNode):
	def __init__(self, tag, children, props = None):
		if not tag or not children:
			raise ValueError("tag and children are required")
		super().__init__(tag = tag, value = None, children = children, props = props)

	def to_html(self):
		children = "".join(child.to_html() for child in self.children)
		return f"<{self.tag}>{children}</{self.tag}>"





