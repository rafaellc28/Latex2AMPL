#!/usr/bin/python -tt

import lexer
import parser
import ply.lex as lex
import ply.yacc as yacc
import sys
import re

from CodeSetup import *
from CodeGenerator import *

DEBUG = False

lexer = lex.lex(module=lexer)
parser = yacc.yacc(module=parser)
#parser.defaulted_states = {}

for arg in sys.argv:
	if arg == "-d":
		DEBUG = True

doc = sys.stdin.read()

# Set up a logging object
import logging
logging.basicConfig(
    level = logging.DEBUG,
    filename = "parselog.txt",
    filemode = "w",
    format = "%(filename)10s:%(lineno)4d:%(message)s"
)
log = logging.getLogger()

doc = re.sub(',\s*\\\\\\\\', ', ', doc)

result = parser.parse(doc, debug=log)

if DEBUG:
	print(result)

if result:
	if not DEBUG:
		try:
			codeGenerator = CodeGenerator()
			result.setupEnvironment(CodeSetup(codeGenerator))
			response = result.generateCode(codeGenerator)
			print(response)
		except:
			print("Error while generating MathProg code. Please, check your Latex code!")
	else:
		codeGenerator = CodeGenerator()
		result.setupEnvironment(CodeSetup(codeGenerator))
		response = result.generateCode(codeGenerator)
		print(response)
