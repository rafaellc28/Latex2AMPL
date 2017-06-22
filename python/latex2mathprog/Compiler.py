#!/usr/bin/python -tt

import ply.lex as lex
import ply.yacc as yacc
import lexer as lexer
import parser as parser
import re
import logging

from SyntaxException import *
from CodeSetup import *
from CodeGenerator import *

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

		self.lexer.lineno = 1
		res = ""
		doc = re.sub(',\s*\\\\\\\\', ', ', doc)
		lines = doc.split("\n")
		result = None

		try:
			result = self.parser.parse(doc, debug=self.log)
		except SyntaxException as msg:
			if msg[0] == "EOF":
				res += "Syntax error at EOF."
			else:
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
				except CodeGenerationException as msg:
					res += msg
				except:
					res += "Error while generating MathProg code. Please, check your Latex code!"
			else:
				if self.DEBUG:
					res += str(result)

				codeGenerator = CodeGenerator()
				result.setupEnvironment(CodeSetup(codeGenerator))
				response = result.generateCode(codeGenerator)
				res += response

		return res
