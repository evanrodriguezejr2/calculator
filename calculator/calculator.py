from utils.graphics import *
from utils.buttons import Button


def main():
	calc = Calculator()
	calc.run()

class Calculator:
	def __init__(self):
		# window
		self.win = GraphWin("Calculator", 500, 700)
		self.win.setBackground("blue")
		self.win.setCoords(0,0,6,8)

		# buttons
		self.bspecs = [(1,1,'+/-'), (2,1,'0'), (3,1,'.'), (4,1,'+'), (1,2,'1'), (2,2,'2'), (3,2,'3'), (4,2,'-'), 
			(1,3,'4'), (2,3,'5'), (3,3,'6'), (4,3,'*'), (5,3,'<<'), (1,4,'7'), (2,4,'8'), (3,4,'9'), (4,4,'/'), 
			(5,4,'C')]
		self.buttons = []
		for (cx, cy, label) in self.bspecs:
			b = Button(self.win, Point(cx, cy), 0.75, 0.75, label)
			self.buttons.append(b)
		self.buttons.append(Button(self.win, Point(5,1.5), .75,1.5,'='))

		# display
		self.display = CalcDisplay(self.win, background_color="lightgray", text_color="white")

	def run(self):
		# Update the display when one of the buttons is clicked
		while True:
			pt = self.win.checkMouse()
			if pt:
				for button in self.buttons:
					if button.clicked(pt):
						self.display.update(button)


class CalcDisplay:
	def __init__(self, win, background_color, text_color):
		self.win = win
		self.background_color = background_color
		self.text_color = text_color
		self.background = Rectangle(Point(.75,5),Point(5.25,7.5))
		self.background.setFill(self.background_color)
		self.background.setOutline("white")

		# current number entered
		self.num = "" 								
		self.num_text = Text(Point(3,6), "") 		
		self.sigdigs = 8 	# precision 

		# current formula entered
		self.formula = "" 							
		self.formula_text = Text(Point(3,7), "") 

		self.op = "" 	 	# last operator selected (+,-,*,/,=)

		# font sizes
		self.num_fontsize = 36
		self.formula_fontsize = 12

		# max character lengths
		self.num_length = 12 
		self.formula_length = 40 

		self.num_text.setSize(self.num_fontsize)
		self.formula_text.setSize(self.formula_fontsize)
		self.background.draw(self.win)
		self.num_text.draw(self.win)
		self.formula_text.draw(self.win)

	def update(self, button):
		# Updates display based on button pressed

		label = button.getLabel()

		nums = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.']
		arith_ops = ['+', '-', '*', '/']

		if label in nums: 
			if self.op: 	# if last selection was operator
				if self.op.getLabel() == '=':
					self.num = ""
					self.formula = ""	
			if len(self.num) < self.sigdigs and len(self.formula) < self.formula_length:
				self.num = self.num + label
				self.formula = self.formula + label

			self._deselectOp()
			self._redrawNum()
			self._redrawFormula()

		elif label in arith_ops:
			if self.op:
				if self.op.getLabel() in arith_ops:
					self.formula = self.formula[:-1]

			self.formula = self.formula + label
			self.num = ""
			self._deselectOp()
			self.op = button
			self.op.setColor("gray")
			self._redrawNum()
			self._redrawFormula()	

		elif label == '+/-':
			if self.num:	# if number is being entered
				self.formula = self.formula[:-len(self.num)]
				if self.num[0] == '-':
					self.num = self.num[1:]
				else:
					self.num = '-' + self.num
				self.formula += self.num
			else:
				self.num += '-'
				self.formula += '-'

			self._deselectOp()
			self._redrawNum()
			self._redrawFormula()

		elif label == 'C':
			self.num = ""
			self.formula = ""
			self._deselectOp()
			self._redrawNum()
			self._redrawFormula()

		elif label == '<<':
			if self.num:
				self.num = self.num[:-1]
			self.formula = self.formula[:-1]
			self._deselectOp()
			self._redrawNum()
			self._redrawFormula()
		
		elif label == '=':
			try:
				result = f"{eval(self.formula):.8g}"
				self.num = result
				self.formula = result
				self._deselectOp()
				self.op = button
				self._redrawNum()
				self._redrawFormula()
			except:
				self.num = ""
				self.formula = ""
				self._deselectOp()
				self._setNum("ERROR")

	def _redrawNum(self):
		self.num_text.setText(self.num.ljust(self.num_length))

	def _setNum(self, s):
		self.num_text.setText(str(s))

	def	_redrawFormula(self):
		self.formula_text.setText(self.formula.ljust(self.formula_length))

	def _deselectOp(self):
		# Deselects last selected operator
		if self.op:
			self.op.setColor("black")
			self.op = ""


if __name__ == "__main__":
	main()