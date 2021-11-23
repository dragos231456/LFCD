
class TreeNode:
	def __init__(self, index, info, parent, left_sibling):
		self.index = index
		self.info = info
		self.parent = parent
		self.left_sibling = left_sibling

	def toList(self):
		return [str(self.index), self.info, str(self.parent), str(self.left_sibling)]

	def __str__(self):
		return str(self.index) + ", " + str(self.info) + ", " + str(self.parent) + ", " + str(self.left_sibling)