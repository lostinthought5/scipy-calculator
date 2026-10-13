# neccessary to install sympy library and set up virtual environment if needed

'''
For this project, I used the sympy library, basically a better version of
the math library. It's capable of doing algebra and integration quite easily.
I used the SymPy documentation as a reference!
'''

import sympy, re
from sympy import sin, cos, tan, log, pi, sympify, integrate, E, sqrt, symbols
from sympy.core.sympify import SympifyError

"""
class HistoryNode():
	def __init__(self, order, user_inp, ans):
		self.order = order
		self.user_inp = user_inp
		self.ans = ans
		self.left, self.right = None, None

class HistoryBST():
	def __init__(self):
		self.root = None
		self._next_order = 1 # this is to track the order of node insertion

	def insert(self, user_inp, ans):
		order = self._next_order
		self._next_order += 1 # increases order number for next node
		self.root = self._insert(self.root, order, user_inp, ans)

	def _insert(self, node, order, user_inp, ans):
		if node is None:
			return HistoryNode(order, user_inp, ans)
		
		if ans < node.ans:
			node.left = self._insert(node.left, order, user_inp, ans)

		elif ans > node.ans:
			node.right = self._insert(node.right, order, user_inp, ans)

		else:
			node.ans = ans

		return node

	def search(self, ans):
		return self._search(self.root, ans)

	def _search(self, node, ans):
		if node is None:
			return None
		
		elif ans == node.ans:
			return node
		
		elif ans < node.ans:
			return self._search(node.left, ans)
		
		elif ans > node.ans:
			return self._search(node.right, ans)

	def _traversal(self, node, array): # traversal order irrelevant here, purpose is to create node list
		if node is None:
			return

		self._traversal(node.left, array)
		array.append(node)
		self._traversal(node.right, array)

	def el_sorted(self): # sorts based on earliest to latest node
		nodes = []
		self._traversal(self.root, nodes)
		nodes.sort(key=lambda node: node.order) # sorting based on the nodes' order numbers
		return nodes

	def le_sorted(self):
		nodes = self.el_sorted()
		return reversed(nodes) # reverses the order of the list
"""


class Calculator():
	def __init__(self):
		# these values should be private

		# self.history = HistoryBST()
		self.active: bool = True
		# self.current_option = None

		self.accepted_inputs: dict[str, function] = {
			'a' : lambda: self.solver('a'),
			'i' : lambda: self.solver('i'),
			# 'h' : self.history,
			'q' : self.quit,
		}

	def start(self):
		print('Hello and welcome. This calculator may be used for basic math, trigonometry, and basic integrals!')

		while self.active:
			print("What kind of calculation/option is needed?")
			user_input: str = input("Arithmetic & Trigonometry (a) | Integration (i) |" 
			                   "History (h) | Exit (q) | ").strip().lower() # corrects input

			if not (user_input in self.accepted_inputs):
				print("Please enter a valid option!")
				continue

			self.accepted_inputs[user_input]()
			print() # just to differentiate between entries in terminal

	def quit(self):
		print("Thank you for using me! Good bye!")
		self.active = False

	def is_valid_input(self, user_input: str) -> bool:
		new_input = user_input.replace(" ", "").strip() # this removes all spacing whether visible or not

		# using regex here; only permitted characters
		if not re.match(r'^[0-9x\+\-\*\/\^\(\)\.a-zA-Z]+$', new_input):
			return False
		return True

	def solver(self, input_type: str):
		callbacks: dict[str: function] = {
			'a' : self.arithmetic,
			'i' : self.integrals,
		}

		user_problem: str = input("Please enter your problem: ")
		
		if not (self.is_valid_input(user_problem)):
			print("Invalid characters detected; only numbers, operators, letters, and parenthesis permitted!")
			return

		try:
			expression = sympify(user_problem) # the documentation says sympify uses eval(); avoid in production
			callbacks[input_type](expression)

		except ZeroDivisionError: # should handle different exception cases to print for each
			print("Cannot divide by zero, please try again!")

		except SympifyError:
			print("Invalid syntax detected; make sure your problem is properly formatted!")

		except Exception as e:
			print("BROKE! ERROR: " + e)
			
	def arithmetic(self, expr: object):
		answer = expr.evalf()
		print(f"Solution: {answer:.4f}")

	def integrals(self, expr: object):
		x = symbols('x')

		if expr.free_symbols - {x}:
			print("For basic integrals, only functions of x may be integrated!")
			return

		answer = integrate(expr, x)
		print(f"Solution: {answer}")

		# self.history.insert(user_inp, ans)

if __name__ == '__main__':
	calculator = Calculator()
	calculator.start()



"""
elif type_input == 'h':
user_input = input('Display all history or search for solution? (a / s) | ')
print()

if user_input == 'a':
	user_input = input('Display from earliest to latest or vise versa? (e-l / l-e) | ')
	print()

	if user_input == 'e-l':
		nodes = calculator.history.el_sorted() # gathers e-l sorted list from history

		for node in nodes:
			print(f'{node.order}. User problem: {node.user_inp} | Solution: {node.ans}')
		print()
		
	elif user_input == 'l-e':
		nodes = calculator.history.le_sorted() # gathers l-e sorted list from history

		for node in nodes:
			print(f'{node.order}. User problem: {node.user_inp} | Solution: {node.ans}')
		print()

	else:
		print('Please enteer a valid option!\n')

elif user_input == 's':
	ans = float(input("Enter entry's solution to search for: "))
	node = calculator.history.search(ans) # searches for ans in calculator's history BST
	print(f'User problem: {node.user_inp} | Solution: {node.ans}\n') # prints entry for provided solution

else: 
	print('Please enter a valid option!\n')
"""
		