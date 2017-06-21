#!/usr/bin/python -tt

#from os import sys, path
#sys.path.append(path.dirname(path.abspath(__file__)))

#from Lexer import *
import ply.lex as lex
import ply.yacc as yacc
import latex2mathprog.lexer as lexer
import latex2mathprog.parser as parser
import re
import logging

from latex2mathprog.SyntaxException import *
from latex2mathprog.CodeSetup import *
from latex2mathprog.CodeGenerator import *

class Compiler:

	def __init__(self, DEBUG = False):
		self.DEBUG = DEBUG

		#self.lexer = Lexer()
		self.lexer = lex.lex(module=lexer)
		self.parser = yacc.yacc(module=parser)
		self.parser.defaulted_states = {}

		# Set up a logging object
		logging.basicConfig(
		    level = logging.DEBUG,
		    filename = "parselog.txt",
		    filemode = "w",
		    format = "%(filename)10s:%(lineno)4d:%(message)s"
		)
		self.log = logging.getLogger()

	def compile(self, doc):

		res = ""
		doc = re.sub(',\s*\\\\\\\\', ', ', doc)
		lines = doc.split("\n")
		result = None

		try:
			result = self.parser.parse(doc, debug=self.log)
		except SyntaxException, msg:
			lineNum = msg[0]-1
			line = lines[lineNum]

			totalCharLinesAbove = 0
			lineNum -= 1
			while lineNum >= 0:
				totalCharLinesAbove += len(lines[lineNum])+1
				lineNum -= 1
						
			res += "Syntax error at line %d, position %d: '%s'.\nContext: %s." % (msg[0], msg[1]-totalCharLinesAbove+1, msg[2], line)

		if result:
			if not self.DEBUG:
				try:
					codeGenerator = CodeGenerator()
					result.setupEnvironment(CodeSetup(codeGenerator))
					response = result.generateCode(codeGenerator)
					res += response
				except CodeGenerationException, msg:
					res += msg
				except:
					res += "Error while generating MathProg code. Please, check your Latex code!"
			else:
				res += str(result)
				codeGenerator = CodeGenerator()
				result.setupEnvironment(CodeSetup(codeGenerator))
				response = result.generateCode(codeGenerator)
				res += response

		return res
