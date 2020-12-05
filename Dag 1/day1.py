import io
import sys
		
class SearchTreeNode:
	def __init__(self, value):
		self.value = value
		self.left = None
		self.right = None
		
	def add_child_node(self, node):
		if node.value < self.value:
			if self.left == None:
				self.left = node
			else:
				self.left.add_child_node(node)
		else:
			if self.right == None:
				self.right = node
			else:
				self.right.add_child_node(node)
				
	def __iter__(self):
		if self.left != None:
			yield from self.left
		yield self.value
		if self.right != None:
			yield from self.right
				
class SearchTree:
	def __init__(self):
		self.root = None
		
	def add(self, value):
		node = SearchTreeNode(value)
		if self.root == None:
			self.root = node
		else:
			self.root.add_child_node(node)
			
	def __iter__(self):
		if self.root != None:
			yield from self.root
			
def first(file_name):
	search_tree = SearchTree()
	with io.open(file_name, 'r') as infile:
		for line in infile:
			search_tree.add(int(line))
	numbers = list(search_tree) # Simplify iteration
	target = 2020
	index_s = 0
	index_l = -1
	small = numbers[index_s]
	large = numbers[index_l]
	index_s_raised = False # Whenever we lower index_l, we need to backtrack on index_s to make sure we didn't overstep the solution
	# Time complexity: N
	while small + large != target:
		if small + large < target:
			index_s += 1
			index_s_raised = True
		elif index_s_raised or index_s == 0:
			index_l -= 1
			index_s_raised = False
		else:
			index_s -= 1
		small = numbers[index_s]
		large = numbers[index_l]
	print("First star: {}".format(small * large))

def second(file_name):
	search_tree = SearchTree()
	with io.open(file_name, 'r') as infile:
		for line in infile:
			search_tree.add(int(line))
	numbers = list(search_tree) # Simplify iteration
	target = 2020
	index_s = 0
	index_m = 1
	index_l = len(numbers) - 1
	small = numbers[index_s]
	medium = numbers[index_m]
	large = numbers[index_l]
	"""
	Raise index_m to the first value for this index_s and index_l which produces a too large result.
	Run the algorithm in the first solution on index_s and index_m.
	If they meet, reset index_s to 0 and index_m to index which produced the too large result, lower index_l and start over.
	
	Time complexity N^2
	"""
	last_too_large_index_m = 0
	index_s_raised = False
	while small + medium + large != target:
		if small + medium + large < target:
			if index_m + 1 < index_l:
				index_m += 1
			else:
				index_s += 1
				small = numbers[index_s]
				while small + medium + large > target and index_m - 1 > index_s:
					index_m -= 1
					medium = numbers[index_m]
		else:
			last_too_large_index_m = index_m
			while small + medium + large != target:
				if small + medium + large < target:
					index_s += 1
				else:
					index_m -= 1
					medium = numbers[index_m]
					while small + medium + large > target and index_s > 0:
						index_s -= 1
						small = numbers[-1]
				if index_s == index_m:
					index_s = 0
					index_m = last_too_large_index_m
					index_l -= 1
					break
				small = numbers[index_s]	
		small = numbers[index_s]
		medium = numbers[index_m]
		large = numbers[index_l]
	print("Second star: {}".format(small * medium * large))
			
if (__name__ == '__main__'):
	first(sys.argv[1])
	second(sys.argv[1])