# neccessary to install sympy library and set up virtual environment if needed

'''
For this project, I used the sympy library, basically a better version of
the math library. It's capable of doing algebra and integration quite easily.
I used the SymPy documentation as a reference!
'''

import sympy as sm
from sympy import sin, cos, tan, log, pi, sympify, integrate, E, sqrt, symbols
from sympy.core.sympify import SympifyError

allowed = {
'sin': sin,
'cos': cos,
'tan': tan,
'log': log,
'pi': pi,
'π': pi,
'E': E,
'e': E,
'sqrt': sqrt,
}

class HistoryNode():
	def __init__(self, order, user_inp, ans):
		self.order = order
		self.user_inp = user_inp
		self.ans = ans
		self.left, self.right = None, None

class Calculator():
	def __init__(self):
		self.history = HistoryBST()

	def arithmetic(self, user_inp):
		try:
			ans = sympify(user_inp, locals=allowed).evalf() # evaluates expression with vars only in allowed

			try:
				if ans == float(user_inp): # no arithmetic to perform
					print('Please input a valid problem!\n')
					return None # done since otherwise ans will be printed in main

			except: # must otherwise contain more than 1 char
				pass

			if ans.free_symbols: # if sympify has defined variables not in "allowed" dict
				raise SympifyError('Error from having invalid characters inputted!')

			else:
				self.history.insert(user_inp, float(ans))
				return float(ans)

		except SympifyError:
			print('Please input a valid problem!\n')

	def integral(self, user_inp):
		try:
			x = symbols('x')
			expr = sympify(user_inp, locals=allowed) 

			if expr.free_symbols - {x}: # if sympify has defined variables not in "allowed" dict besides x
				raise SympifyError('Error from having invalid characters inputted!')
		
			else:
				self.history.insert(user_inp, ans)
				return integrate(expr, x)

		except SimpifyError:
			print('Error during intergration, please input properly!\n')

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

if __name__ == '__main__':
	calculator = Calculator()
	print('Hello and welcome. This calculator may be used for basic math up to basic integrals!')

	while True:
		type_input = input('What kind of calculation/option is needed?\nArithmetics'
							' (a) / Integration (i) / History (h) / Exit (q) | ').strip().lower() # corrects input
		print()

		if type_input == 'a': # should be able to handle any problems containing trigonometry, pi or e
			user_input = input('Input your problem: ')
			ans = calculator.arithmetic(user_input)

			if ans or ans == 0: # necessary to avoid 'return None' from affecting ans
				print(f'Solution: {ans}\n')

		elif type_input == 'i':
			user_input = input('Input your expression: ')
			ans = calculator.integral(user_input)

			if ans or ans == 0:
				print(f'Solution: {ans}\n')

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

		elif type_input == 'q':
			print('Goodbye! Thanks for using me!')
			break
			
		else:
			print('Please enter a valid option!\n')