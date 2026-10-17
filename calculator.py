from sympy import sin, cos, tan, log, pi, sympify, integrate, E, sqrt, symbols, Integral
from sympy.core.numbers import ComplexInfinity, NaN
from sympy.core.sympify import SympifyError
from re import match

class Calculator():
	def __init__(self):
		self.history: list = []
		self.active: bool = True
		self.current_option: str = None

		self.option_types: dict[str, str] = {
			'e' : "(Standard Expressions)",
			'i' : "(Integration)",
			'h' : "(History)",
		}

		self.accepted_inputs: dict[str, callable] = {
			'e' : lambda: self.solution_handler('e'),
			'i' : lambda: self.solution_handler('i'),
			'h' : self.history_handler,
			'q' : self.quit,
		}

		self.accepted_operations: dict[str, object] = {
			'pi' : pi,
			'e' : E,
			'sin' : sin,
			'cos' : cos,
			'tan' : tan,
			'log' : log,
			'sqrt' : sqrt,
		}

	def start(self):
		print('Hello and welcome. This calculator may be used for basic math, trigonometry, and basic integrals!\n')

		user_input: str = "" # done to update the var rather than define per iteration
		while self.active:
			if not self.current_option:
				print("(Menu) - What kind of calculation/option is needed?")
				user_input = input("Standard Expressions - (e) | Integration (i) | " 
			                   		"History (h) | Exit (q) | ").strip().lower() # corrects input

				if not (user_input in self.accepted_inputs):
					print("Please enter a valid option!\n")
					continue

				print() # for terminal spacing

				if user_input == 'q':
					self.accepted_inputs['q']()
					continue

				self.current_option = self.option_types[user_input]

			self.accepted_inputs[user_input]()

	def quit(self):
		print("Thank you for using me! Good bye!\n")
		self.active = False

	def withdraw(self):
		print() # terminal spacing
		self.current_option = None

	def is_valid_input(self, user_input: str) -> bool:
		new_input = user_input.replace(" ", "").strip() # this removes all spacing whether visible or not

		# using regex here; only permitted characters
		if not match(r'^[0-9x\+\-\*\/\^\(\)\.a-zA-Z]+$', new_input):
			return False
		return True

	def solution_handler(self, input_type: str): # input_type = e or i
		solution_methods: dict[str, callable] = {
			'e' : self.evaluate,
			'i' : self.integrate,
		}
		
		user_problem: str = input(f"{self.current_option} - Please enter your problem | Go Back (b): ").strip().lower()
		print()
		
		if not (self.is_valid_input(user_problem)):
			print("Invalid characters detected; only numbers, operators, letters, and parenthesis permitted!\n")
			return
		
		try:
			func = solution_methods[input_type]
			self.withdraw() if user_problem == 'b' else func(user_problem)

		except ZeroDivisionError:
			print("Cannot divide by zero, please try again!\n")

		except SympifyError:
			print("Invalid syntax detected; make sure your problem follows standard formatting!\n")

		except Exception as error:
			print(f"Unaccounted for error occurred: {error}")
			
	def evaluate(self, user_input: str):
		# the documentation says sympify uses eval(); avoid in production
		expression: object = sympify(user_input, locals = self.accepted_operations, evaluate = False)

		if expression.is_Number:
			print("Single numbers are not allowed, please try again!\n")
			return
		
		if expression.free_symbols: # this checks for non-numerical characters
			print("Variables are not allowed in standard expressions, please try again!\n")
			return

		answer: object = sympify(user_input, locals = self.accepted_operations) # evaluates for the actual answer

		if isinstance(answer, (ComplexInfinity, NaN)): # checks whether var corresponds to classes representing infinity
			print("Your expression is undefined, please try again!\n")
			return

		if answer.is_real is False:
			print("Complex numbers are not allowed, please try again!\n")
			return
		elif answer.is_real is None: # .is_real is None when sympy can't determine
			raise SympifyError("")

		print(f"Solution: {answer:.4f}\n")
		self.history.append(f"Input = {user_input} - Solution = {answer:.4f}")

	def integrate(self, user_input: str):
		allowed_operations = self.accepted_operations.copy()

		x = symbols('x', real = True) # must clarify x is real, otherwise .is_real logic works differently
		allowed_operations['x'] = x

		expression = sympify(user_input, locals = allowed_operations)

		if expression.free_symbols - {x}: 
			print("Only syntax in terms of functions of x is accepted, please try again!\n")
			return

		if isinstance(expression, (ComplexInfinity, NaN)):
			print("Your expression is undefined, please try again!\n")
			return

		answer = integrate(expression, x)

		if isinstance(answer, Integral):
			print("Your expression is undefined, please try again!\n")
			return
		
		if not answer.is_real:
			print("Complex numbers are not allowed, please try again!\n")
			return

		print(f"Solution: {answer} + C\n")

		self.history.append(f"Input = {user_input} - Solution = {answer}")


	def history_handler(self):
		if not self.history:
			print("There are no recorded problem entries yet!\n")
			self.withdraw()
			return

		array = self.history.copy()
		array_types : dict[str, list] = {
			'e' : array, 
			'l' : reversed(array),
		}

		# can just print History here since it is guaranteed to be that option
		print("(History) - Would you like to:")
		user_input = input("Display Earliest Entries (e) | Latest Entries (l) "
							"| Go Back (b): ").strip().lower()
		print()

		if not user_input in array_types:
			print("Please input a valid history option!")
			return
		elif user_input == 'b':
			self.withdraw()
			return

		print("History:")

		for entry in array:
			print(entry)

		print()

if __name__ == '__main__':
	calculator = Calculator()
	calculator.start()